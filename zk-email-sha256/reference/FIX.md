# Fix / finding: zk-email SHA256 templates (zkSecurity #02)

Source: zkSecurity audit of zkemail/zk-email-verify, 2024-05, finding #02, pages 24-26.
Vulnerable commit `f2fb77c`; fixed by `ad0ad6`/`e14e88`/`d667a1` (merge `95cd90`).

## Report excerpt

# 02 - SHA256 templates can be made return 0 on arbitrary inputs
zk-email-verify/packages/circuits/lib/sha.circom
High
Description
Both custom SHA256 templates `Sha256General` and `Sha256Partial`, as well as their bytes variants `Sha256Bytes` and `Sha256BytesPartial`, are vulnerable to an attack where the prover passes in a maliciously crafted `paddedInLength` which causes the returned hash result to be the all-zeros bit array.
In `Sha256General` and `Sha256Partial`, `paddedInLength` represents the bit length of the input message. It is connected to a newly created signal `inBlockIndex` by the constraint
inBlockIndex <-- (paddedInLength >> 9); paddedInLength === inBlockIndex * 512;
SHA2 operates on the input in chunks, and `inBlockIndex` represents the number of chunks to be hashed. To support inputs of dynamic length, the template stores the intermediate hash result after each chunk, and at the end selects which one to return, using the `ItemAtIndex` template. This is done for each output bit:
component arraySelectors[256]; for (k=0; k<256; k++) {
arraySelectors[k] = ItemAtIndex(maxBlocks); for (j=0; j<maxBlocks; j++) {
arraySelectors[k].in[j] <== sha256compression[j].out[k]; } arraySelectors[k].index <== inBlockIndex - 1; // The index is 0 indexed and the block numbers are 1 indexed. out[k] <== arraySelectors[k].out; }
The exploit we found manages to set `inBlockIndex - 1` to a large number close to the native modulus. In particular, the index is larger than the array size `maxBlocks`. On an index that exceeds the array bounds, the output of `ItemAtIndex` is zero. Therefore, the hash result ends up being an array of 0 bits -- regardless of the input value.
The issue is that `ItemAtIndex` does not properly constrain the index to lie in its intended range:
template ItemAtIndex(maxArrayLen) { // ... signal input index; // ...

// Ensure that index < maxArrayLen component lessThan = LessThan(bitLength); lessThan.in[0] <== index; lessThan.in[1] <== maxArrayLen; lessThan.out === 1;
As we can see in this code excerpt, `index` is passed to `LessThan(bitLength)`. For `LessThan` to be sound, both inputs have to fit in `bitLength` bits. However, this property is never checked on the `index`.
Adding to the misfortune, the SHA2 input bit length `paddedInLength` is passed to an instance of `LessThan` as well, with the same mistake of not constraining its bit range (in `Sha256General` and `Sha256Partial`).
Generally speaking, when using `LessThan` without a bit constraint, small "negatives" modulo the field size p, like -1  p - 1, are treated as being less than a small positive value. A detailed analysis of the SHA256 templates
reveals that no constraints prevent `inBlockIndex` to be one of the following values:
-5, ... , -1, 0
These values are able to trick both instances of `LessThan` (the one for `paddedInLength` and the one for `index`) into returning 1, which is incorrect.
To exploit this in an isolated instance of `Sha256Bytes`, the prover just has to:
pass in one of -5  64, ... , -64, 0 as `paddedInLength` (note: this is multiplied by 8 in `Sha256Bytes`)
change the `inBlockIndex` witness generation code to work for the negative case:
- inBlockIndex <-- (paddedInLength >> 9); + inBlockIndex <-- (paddedInLength / 512);
With this simple attack, we are able to create a valid proof that the SHA256 output consists of all zeros, regardless of its input.
Impact
Meaningfully exploiting this issue in `EmailVerifer` is infeasible, because `AssertZeroPadding` is also used on the two SHA256 input lengths (`emailHeaderLength` and `emailBodyLength`), and given small negative lengths implies that the email header or body consists of all zeros. However, consumers of the zk-email-verify library which use SHA256 templates in a different context may be vulnerable to the attack.
Recommendation
In `ItemAtIndex`, remove `LessThan` and instead add an assertion that the sum of all `eqs[i]` equals 1. This proves that the index to select is one of the array indices.
In all SHA256 templates, document the assumption that `paddedInLength` is constrained to a certain number of

bits:
`ceil(log2(maxBitLength))` bits in the case of `Sha256General` and `Sha256Partial` `ceil(log2(8 * maxByteLength))` bits in the case of `Sha256Bytes` and `Sha256BytesPartial` In `EmailVerifier`, use `Num2Bits` to constrain both `emailHeaderLength` and `emailBodyLength` to appropriate bit lengths, right after those signals are introduced.
Client response
The issue was fixed in commits ad0ad6, e14e88 and d667a1.


## Fix diff: sha.circom

```diff
diff --git a/packages/circuits/lib/sha.circom b/packages/circuits/lib/sha.circom
index af9fadd..a2bf4ef 100644
--- a/packages/circuits/lib/sha.circom
+++ b/packages/circuits/lib/sha.circom
@@ -11,9 +11,9 @@ include "../utils/functions.circom";
 
 /// @title Sha256Bytes
 /// @notice Computes the SHA256 hash of input bytes
-/// @input paddedIn: Message to hash padded as per the SHA256 specification
-/// @input paddedInLength: Length of the message in bytes including padding
-/// @output out: The 256-bit hash of the input message
+/// @input paddedIn Message to hash, padded as per the SHA256 specification; assumes to consist of bytes
+/// @input paddedInLength Length of the padded message; assumes to be in `ceil(log2(8 * maxByteLength))` bits
+/// @output out The 256-bit hash of the input message
 template Sha256Bytes(maxByteLength) {
     signal input paddedIn[maxByteLength];
     signal input paddedInLength;
@@ -40,12 +40,13 @@ template Sha256Bytes(maxByteLength) {
 
 /// @title Sha256BytesPartial
 /// @notice Computes the SHA256 hash of input bytes with a precomputed state
-/// @input paddedIn Message to hash padded as per the SHA256 specification
-/// @input paddedInLength Length of the message in bytes including padding
+/// @input paddedIn Message to hash padded as per the SHA256 specification; assumes to consist of bytes
+/// @input paddedInLength Length of the padded message; assumes to be in `ceil(log2(8 * maxByteLength))` bits
 /// @input preHash The precomputed state of the hash
 /// @output out SHA hash the input message with the precomputed state
 template Sha256BytesPartial(maxByteLength) {
     assert(maxByteLength % 32 == 0);
+
     signal input paddedIn[maxByteLength];
     signal input paddedInLength;
     signal input preHash[32];
@@ -82,15 +83,15 @@ template Sha256BytesPartial(maxByteLength) {
 /// @title Sha256General
 /// @notice A modified version of the SHA256 circuit that allows specified length messages up to a 
 ///         max to all work via array indexing on the SHA256 compression circuit.
-/// @input paddedIn: Message to hash padded as per the SHA256 specification
-/// @input paddedInLength: Length of the message in bits including padding
-/// @output out: The 256-bit hash of the input message
+/// @input paddedIn Message to hash padded as per the SHA256 specification; assumes to consist of bits
+/// @input paddedInLength Length of the padded message; assumes to be in `ceil(log2(maxBitLength))` bits
+/// @output out The 256-bit hash of the input message
 template Sha256General(maxBitLength) {
-    // maxBitLength must be a multiple of 512, and the bit circuits in this file are limited to 15 so must be raised if the message is longer.
+    // maxBitLength must be a multiple of 512
+    // the bit circuits in this file are limited to 15 so must be raised if the message is longer.
     assert(maxBitLength % 512 == 0);
-    var maxBitsPaddedBits = log2Ceil(maxBitLength);
-    assert(2 ** maxBitsPaddedBits > maxBitLength);
 
+    var maxBitsPaddedBits = log2Ceil(maxBitLength);
 
     // Note that maxBitLength = maxBits + 64
     signal input paddedIn[maxBitLength];
@@ -204,15 +205,16 @@ template Sha256General(maxBitLength) {
 
 /// @title Sha256Partial
 /// @notice Calculates the SHA256 hash of a message with a precomputed state
-/// @input paddedIn: Message to hash padded as per the SHA256 specification
-/// @input paddedInLength: Length of the message in bits including padding
-/// @input preHash: The precomputed state of the hash
-/// @output out: The 256-bit hash of the input message
+/// @input paddedIn Message to hash padded as per the SHA256 specification; assumes to consist of bits
+/// @input paddedInLength Length of the padded message; assumes to be in `ceil(log2(maxBitLength))` bits
+/// @input preHash The precomputed state of the hash; assumes to consist of bits
+/// @output out The 256-bit hash of the input message
 template Sha256Partial(maxBitLength) {
-    // maxBitLength must be a multiple of 512, and the bit circuits in this file are limited to 15 so must be raised if the message is longer.
+    // maxBitLength must be a multiple of 512
+    // the bit circuits in this file are limited to 15 so must be raised if the message is longer.
     assert(maxBitLength % 512 == 0);
+
     var maxBitsPaddedBits = log2Ceil(maxBitLength);
-    assert(2 ** maxBitsPaddedBits > maxBitLength);
 
     // Note that maxBitLength = maxBits + 64
     signal input paddedIn[maxBitLength];
```

## Fix diff: array.circom (ItemAtIndex)

```diff
diff --git a/packages/circuits/utils/array.circom b/packages/circuits/utils/array.circom
index 042234b..d743aaa 100644
--- a/packages/circuits/utils/array.circom
+++ b/packages/circuits/utils/array.circom
@@ -7,27 +7,20 @@ include "./functions.circom";
 
 /// @title ItemAtIndex
 /// @notice Select item at given index from the input array
-/// @notice This is QuinSelector from MACI https://github.com/privacy-scaling-explorations/maci/
+/// @notice This template that the index is valid
+/// @notice This is a modified version of QuinSelector from MACI https://github.com/privacy-scaling-explorations/maci/
 /// @param maxArrayLen The number of elements in the array
 /// @input in The input array
 /// @input index The index of the element to select
 /// @output out The selected element
 template ItemAtIndex(maxArrayLen) {
-    var bitLength = log2Ceil(maxArrayLen);
-    assert(2 ** bitLength > maxArrayLen);
-
     signal input in[maxArrayLen];
     signal input index;
 
     signal output out;
 
-    // Ensure that index < maxArrayLen
-    component lessThan = LessThan(bitLength);
-    lessThan.in[0] <== index;
-    lessThan.in[1] <== maxArrayLen;
-    lessThan.out === 1;
-
-    component calcTotal = CalculateTotal(maxArrayLen);
+    component calcTotalValue = CalculateTotal(maxArrayLen);
+    component calcTotalIndex = CalculateTotal(maxArrayLen);
     component eqs[maxArrayLen];
 
     // For each item, check whether its index equals the input index.
@@ -36,20 +29,24 @@ template ItemAtIndex(maxArrayLen) {
         eqs[i].in[0] <== i;
         eqs[i].in[1] <== index;
 
-        // eqs[i].out is 1 if the index matches. As such, at most one input to
-        // calcTotal is not 0.
-        calcTotal.nums[i] <== eqs[i].out * in[i];
+        // eqs[i].out is 1 if the index matches - so calcTotal is sum of 0s + 1 * valueAtIndex
+        calcTotalValue.nums[i] <== eqs[i].out * in[i];
+
+        // Take the sum of all eqs[i].out and assert that it is at most 1.
+        calcTotalIndex.nums[i] <== eqs[i].out;
     }
 
-    // Returns 0 + 0 + ... + item
-    out <== calcTotal.sum;
+    // Assert that the sum of eqs[i].out is 1. This is to ensure the index passed is valid.
+    calcTotalIndex.sum === 1;
+
+    out <== calcTotalValue.sum;
 }
 
 
 /// @title CalculateTotal
 /// @notice Calculate the sum of an array
 /// @param n The number of elements in the array
-/// @input nums The input array
+/// @input nums The input array; assumes elements are small enough that their sum does not overflow the field
 /// @output sum The sum of the input array
 template CalculateTotal(n) {
     signal input nums[n];
@@ -70,12 +67,12 @@ template CalculateTotal(n) {
 /// @title SelectSubArray
 /// @notice Select sub array from an array given a `startIndex` and `length`
 /// @notice This is same as `VarShiftLeft` but with elements after `length` set to zero
-/// @notice This is not used in ZK-Email circuits anywhere
+/// @notice This is not used in core ZK-Email circuits at the moment
 /// @param maxArrayLen: the maximum number of bytes in the input array
 /// @param maxSubArrayLen: the maximum number of integers in the output array
-/// @input in: the input byte array
-/// @input startIndex: the start index of the sub array
-/// @input length: the length of the sub array
+/// @input in: the input array
+/// @input startIndex: the start index of the sub array; assumes a valid index
+/// @input length: the length of the sub array; assumes to fit in `ceil(log2(maxArrayLen))` bits
 /// @output out: array of `maxSubArrayLen` size, items starting from `startIndex`, and items after `length` set to zero
 template SelectSubArray(maxArrayLen, maxSubArrayLen) {
     assert(maxSubArrayLen < maxArrayLen);
@@ -86,8 +83,6 @@ template SelectSubArray(maxArrayLen, maxSubArrayLen) {
 
     signal output out[maxSubArrayLen];
 
-    assert(length <= maxSubArrayLen);
-
     component shifter = VarShiftLeft(maxArrayLen, maxSubArrayLen);
     shifter.in <== in;
     shifter.shift <== startIndex;
@@ -114,10 +109,10 @@ template SelectSubArray(maxArrayLen, maxSubArrayLen) {
 /// @input shift The number of indices to shift the array to the left
 /// @output out hifted subarray
 template VarShiftLeft(maxArrayLen, maxOutArrayLen) {
-    var bitLength = log2Ceil(maxArrayLen);
-    assert(2 ** bitLength > maxArrayLen);
     assert(maxOutArrayLen <= maxArrayLen);
 
+    var bitLength = log2Ceil(maxArrayLen);
+
     signal input in[maxArrayLen];
     signal input shift;
 
@@ -149,17 +144,14 @@ template VarShiftLeft(maxArrayLen, maxOutArrayLen) {
 /// @title AssertZeroPadding
 /// @notice Assert that the input array is zero-padded from the given `startIndex`
 /// @param maxArrayLen The maximum number of elements in the input array
-/// @input in The input array
-/// @input startIndex The index from which the array should be zero-padded
+/// @input in The input array;
+/// @input startIndex The index from which the elements should be 0; assumes `startIndex - 1` to fit in `ceil(log2(maxArrayLen))` bits
 template AssertZeroPadding(maxArrayLen) {
     var bitLength = log2Ceil(maxArrayLen);
-    assert(maxArrayLen <= (1 << bitLength));
     
     signal input in[maxArrayLen];
     signal input startIndex;
 
-    assert(startIndex < maxArrayLen);
-    
     component lessThans[maxArrayLen];
 
     for (var i = 0; i < maxArrayLen; i++) {
```

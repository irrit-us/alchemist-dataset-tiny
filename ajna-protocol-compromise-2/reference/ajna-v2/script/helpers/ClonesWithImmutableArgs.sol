// SPDX-License-Identifier: BSD-3-Clause
// Vendored from https://github.com/wighawag/clones-with-immutable-args (same
// library family as the on-chain Ajna factory's clone; only `clone` kept).
// The produced clone appends `data` and a 2-byte length suffix to calldata
// before delegate-calling the implementation, which is exactly what the
// deployed victim pool `0xad24FC773e125Edb223C38a39657cB64bc7C178e` does and
// what `lib/clones-with-immutable-args/src/Clone.sol` reads back.

pragma solidity ^0.8.13;

library ClonesWithImmutableArgs {
    error CreateFail();
    error DataTooLarge();

    uint256 internal constant MAX_CODE_SIZE = 24576;

    function clone(
        address implementation,
        bytes memory data
    ) internal returns (address payable instance) {
        bytes memory creationcode = getCreationBytecode(implementation, data);
        // solhint-disable-next-line no-inline-assembly
        assembly {
            instance := create(0, add(creationcode, 0x20), mload(creationcode))
            if iszero(instance) {
                // revert CreateFail()
                mstore(0x00, 0xebfef188)
                revert(0x1c, 0x04)
            }
        }
    }

    function getCreationBytecode(
        address implementation,
        bytes memory data
    ) internal pure returns (bytes memory ret) {
        unchecked {
            uint256 extraLength = data.length + 2;
            uint256 creationSize = 0x41 + extraLength;
            uint256 runSize = creationSize - 10;
            if (runSize > MAX_CODE_SIZE) {
                revert DataTooLarge();
            }
            uint256 ptr;

            // solhint-disable-next-line no-inline-assembly
            assembly {
                ret := mload(0x40)
                mstore(ret, creationSize)
                mstore(0x40, add(add(ret, 0x20), creationSize))
                ptr := add(ret, 0x20)

                // CREATION (10 bytes)
                // 61 runtime  | PUSH2 runtime (r)
                mstore(
                    ptr,
                    0x6100000000000000000000000000000000000000000000000000000000000000
                )
                mstore(add(ptr, 0x01), shl(240, runSize))

                // 3d 81 60 0a 3d 39 f3 | RETURNDATASIZE DUP2 PUSH1 0x0a RETURNDATASIZE CODECOPY RETURN
                mstore(
                    add(ptr, 0x03),
                    0x3d81600a3d39f33d3d3d3d363d3d376100000000000000000000000000000000
                )
                mstore(add(ptr, 0x13), shl(240, extraLength))

                // RUNTIME (55 bytes + extraLength)
                mstore(
                    add(ptr, 0x15),
                    0x6037363936610000000000000000000000000000000000000000000000000000
                )
                mstore(add(ptr, 0x1b), shl(240, extraLength))

                mstore(
                    add(ptr, 0x1d),
                    0x013d730000000000000000000000000000000000000000000000000000000000
                )
                mstore(add(ptr, 0x20), shl(0x60, implementation))

                mstore(
                    add(ptr, 0x34),
                    0x5af43d3d93803e603557fd5bf300000000000000000000000000000000000000
                )
            }

            // APPENDED DATA
            extraLength -= 2;
            // solhint-disable-next-line no-inline-assembly
            assembly {
                let copyPtr := add(ptr, 0x41)
                let dataPtr := add(data, 0x20)
                let end := add(dataPtr, extraLength)

                for {} lt(dataPtr, end) {} {
                    mstore(copyPtr, mload(dataPtr))
                    copyPtr := add(copyPtr, 0x20)
                    dataPtr := add(dataPtr, 0x20)
                }

                mstore(add(ptr, add(0x41, extraLength)), shl(240, extraLength))
            }
        }
    }
}

# Ajna 部署版源码（媒体称 "Ajna v2"）— 来源与出处

本目录是 **2026-08-28 攻击事件中链上实际运行的 Ajna 池代码**。

**定性更正**：链上实证（对部署区块做二分定位，可按区块号公开复验）表明
这套代码是 **2023 年 7 月的创世（launch）部署**，早于公开仓库的 v1.0.0 tag
（2024-02-17）——它不是"v1.0.0 之后的新版"，而是**比 v1.0.0 更老的遗留版本**。
媒体所称 "Ajna v2" 是报道标签，不对应部署世代；被攻击的是从未升级过的
legacy 池（协议 immutable，无法打补丁）。行为分析、漏洞复现以本目录为准。

## 部署时间（链上二分实证）

| 合约 | 部署区块 | 时间 (UTC) |
|---|---|---|
| 逻辑合约 `0x05bB…9A21` + TakerActions 库 `0x5190…Be9F` | 17,622,995 | 2023-07-04 20:40 |
| 受害 cbETH/WETH 池 `0xad24…178e` | 17,664,706 | 2023-07-10 17:21 |

（Sourcify 的 verifiedAt 只是验证时间，非部署时间。）

## 来源

全部源码取自 Sourcify 验证记录（creation + runtime 均为 `match`），共 6 个源码包。
6 包共享同一套源码树（49 个文件），逐文件哈希校验**零冲突**，故合并为本目录。
（原始源码包已于 2026-09-05 按要求删除；下表地址的 Sourcify 记录公开可查，可随时重新拉取复验。）

## 链上合约 → 角色对照

| 地址 | 角色 | Sourcify matchId | verifiedAt (UTC) |
|---|---|---|---|
| `0x05bB4F6362B02F17C1A3F2B047A8b23368269A21` | ERC20Pool 逻辑合约（编译目标 `src/ERC20Pool.sol:ERC20Pool`） | 2160920 | 2024-08-08 |
| `0x519021054846Cd3D9883359B593b5ed3058Fbe9F` | TakerActions（`take` / `bucketTake`） | — | 2025-06-22 |
| `0x39b8bDd2c2b3409f2D2aBbCc0368691da09eCDD0` | LenderActions（`addQuoteToken` / `removeQuoteToken` 等） | — | 2025-06-21 |
| `0xde6c8171B5b971F71C405631f4e0568Ed8491AAc` | BorrowerActions（`drawDebt` / `repayDebt`） | 6761387 | 2025-07-04 |
| `0x33e5C2b41E915ACfc268A4eaaCC567f612F96601` | KickerActions（`kick`） | — | 2025-06-21 |
| `0x1F172F881EbA06aa7a991651780527c173783cf6` | PoolCommons（利率更新、担保率检查等公共逻辑） | — | 2025-06-21 |
| `0x72bF565f2BdA43294C6cC2BfE17C7FaE5258F819` | LPActions（LP 代币铸造/转移） | 7371091 | 2025-07-14 |
| `0x8B7f874D15c25BeCC4F7c1906b3677533fe60A6e` | SettlerActions（`settle`） | 6627714 | 2025-06-23 |

说明：

- 后 7 行是 `ERC20Pool` 字节码**链接的外部库**，池在运行时以 `delegatecall`
  调用它们（库地址来自 0x05bB 验证元数据的 `settings.libraries` 链接表）。
- LPActions / SettlerActions 未单独下载源码包——其源文件已包含在上述 6 包的
  共享树内（`src/libraries/external/`），且两地址均经 Sourcify 独立确认为 match。
- 受害池：`0xad24FC773e125Edb223C38a39657cB64bc7C178e`（WETH/cbETH），
  攻击 trace 显示其 delegatecall 目标即上表库地址。

## 编译参数（6 包一致）

- compiler: `solc 0.8.18+commit.87f61d96`
- optimizer: enabled, **runs = 0**
- evmVersion: `london`

## 目录结构

- `src/` — 37 个 Solidity 文件（池本体、接口、外部/内部库）
- `lib/` — 依赖（openzeppelin-contracts、clones-with-immutable-args、prb-math，
  即源码树内随包的副本）；另有 2026-09-10 新增的 `lib/forge-std`（v1.8.2，
  仅 PoC 脚本工具，非协议源码）
- `script/` — 2026-09-10 新增的本地 PoC：`AjnaExploit.s.sol`
  （部署→做局→利用→损益证明，详见根目录 README"PoC 与复现材料"）、
  `AjnaExploitExactReplay.s.sol`（移植链上前态的主网逐 wei 精确重放）、
  `generated/ExploitPreState.sol`（由 `verification/generate_prestate_sol.py`
  从 `verification/raw/exploit_prestate_full.json` 生成的 85 槽前态移植库）、
  `helpers/ClonesWithImmutableArgs.sol` 为 clone 工厂（上游 BSD-3-Clause 源码，
  与链上工厂同族：参数附加于 calldata 尾部）
- `foundry.toml` — 为本地工具链补的 remappings；**已用 forge 1.8.1 编译并
  运行上述 PoC 通过**（solc 0.8.18，2026-09-10）

## 与公开仓库 ajna-core 的世系关系（本地对照副本已删除）

**这套部署代码不等于任何公开 tag**（已与 rc1–rc9、v1.0.0 全量 diff 比对），
世系上最接近 rc1–rc3（2023 年春夏）开发线；精确 commit 未公开。关键节点：

- rc1–rc6 及本部署版：`_isCollateralized` **无 1.04 系数**、`takeReserves` 无
  `quoteScale` 参数、无 `AuctionNotTakeable` 检查等；
- rc7–rc9（2023 下半年审计季）起加固：rc9（2024-01-04）已引入
  `COLLATERALIZATION_FACTOR = 1.04`；
- v1.0.0（2024-02-17）继承全部加固，并配套 2024-01 的新工厂部署新池；
- 2023-07 的 legacy 池 immutable，永远停留在加固前的代码——本次被攻击的即此类池。

因此"`_isCollateralized` 无 1.04 系数"等差异是**旧版未被加固**，而非
"新版被私改弱化"：1.04 是后来**加上去**的防护，不是后来**被摘掉**的防护。

## 校验锚点：无精确 GitHub 对应，以链上元数据 keccak256 为准

- **无精确对应的 git commit**（2026-09 复查实证）：`ajna-finance/ajna-core` 的
  master 即 v1.0.0（`0f59e780`），13 个 tag（MVP…v1.0.0）与本树全量 diff 均不吻合；
  组织内 `ajna-repo` 为空仓库（size 0），其余仓库为 keeper/SDK/subgraph/audits；
  GitHub 全局搜索亦无。源码自 2024-08-08 起经 Sourcify 公开可读。
- 权威校验锚点是 **solc 编译元数据**（嵌入链上字节码，Sourcify 据此 full match）：
  每个源文件的 keccak256 + IPFS/Swarm 内容地址。
- 已对本地树做逐文件校验：**49/49 文件 keccak256 与 0x05bB 元数据完全一致**
  （byte-for-byte）。复现方法：对 `ajna-v2/` 内每文件做 keccak256（注意是
  keccak 而非 NIST sha3-256，可用 pycryptodome 的 `Crypto.Hash.keccak`），
  比对 Sourcify 上 0x05bB 合约元数据的 `metadata.sources[path].keccak256`
  （可经 Sourcify API 重新获取）。

## 与 v1.0.0（ajna-core，本地对照副本已删除）的关键行为差异

- `src/libraries/helpers/PoolHelper.sol` 的 `_isCollateralized`（L158-170）：
  部署版（同 rc1–rc6）抵押率阈值为 `collateral×LUP ≥ debt`；v1.0.0 起为
  `≥ 1.04×debt`。这使攻击 setup 交易中两笔 `drawDebt`（各押粉尘 cbETH、借
  49.319073 WETH，债务 = 借款 × 1.0005）得以通过——v1.0.0 下该检查不会放行。
- 注意：1.00 vs 1.04 只降低攻击成本/放宽约束，**不是漏洞边界**；漏洞本体在
  `TakerActions.bucketTake` 的奖励/LP 铸造逻辑（详见根目录 README 的调用路径分析）。

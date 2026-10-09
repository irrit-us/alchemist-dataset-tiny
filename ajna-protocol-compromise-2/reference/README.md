# Ajna Protocol Compromise 2

阅读入口：[经济模型与历史利用链路](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/ECONOMIC_MODEL_AND_EXPLOIT.md>)；[重新获取的链上证据与受验证调用栈](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/VERIFIED_CALLSTACK.md>)（2026-09-08）。本次已取得两笔完整 trace、回执和交易级状态差分，原始数据保存在 `verification/raw/`。下文保留既有历史摘要，其中拍卖公式、第二次 bucketTake 参数、桶余额精确归零、bucketInfo 汇率字段及损益口径存在已更正内容；**冲突时以新验证报告及其原始数据为准**。

## 事件概述

精度补充（2026-09-08）：重新按链上整数和部署版 `Maths.wmul` 计算，A 初次借款时抵押品账面价值比含费债务高 26,314 wei WETH；下文“逐 wei 相等”应理解为极接近边界，不能作为精确整数等式。推导见经济模型笔记的 A 借款边界核算段。

清算边界更正（2026-09-08）：直接解码 setup F129/F134 库调用后确认，A 的 kick 罚金使总债务超过全部存款，LUP 直接变成 `MIN_PRICE`（0.000000099836282890），B 随后按此值接受抵押检查。下文“下滑一档”不准确。详见 `verification/kick_boundary_verification.json` 与经济模型笔记的 B 清算边界段。

2026-08-28，Ethereum 主网上 Ajna Protocol 的 7 个池遭同一手法攻击。媒体报道称之为 "Ajna v2"，但链上实证（部署区块二分定位）：被攻击池是 **2023-07 的创世部署（legacy 池）**，早于公开仓库 v1.0.0 tag（2024-02-17），并非 v1.0.0 之后的新版本。本目录分析 cbETH/WETH 池实例（该池损失约 $124.8K），问题出在 `bucketTake` 的 LP 奖励会计与自建清算拍卖的组合，全战役损失约 $775K。

- **攻击类型（Attack Vector）：** Reward Manipulation —— 攻击者**自建清算拍卖**并使 `bucketTake` 的 LP 奖励按**自抬桶价**计价：先在 bucket 2000（桶价 46,776.65 WETH/cbETH，约市价 4 万倍）存入自有 quote；再构造两笔"立即可清算"的自有仓位并自行 kick；`bucketTake` 按"桶价 − 拍卖价"为 taker 铸造天量 LP（对应 v1.0.0 源码 `TakerActions._rewardBucketTake`），随即 `removeCollateral` 烧 LP 提走真实抵押品；同时一笔仅以 0.001055 cbETH 粉尘抵押品借出的 49.32 WETH 成为坏账，由真实 LP 存款承担。
- **影响范围：** Ethereum 上 7 个配对抵押品池（syrupUSDC、wstETH、rETH、cbETH、WBTC、WETH/USDC、sDAI），合计约 $775.4K。
- **参考：**
  - Defimon 告警与逐池损失表：<https://x.com/DefimonAlerts/status/2093632180656263283>
  - Ajna 官方 acknowledgement：<https://x.com/ajnafi/status/2093730105713377452>

Ajna 协议为 immutable 部署：**没有、也不会有修复版本 commit**，因此本目录不存在漏洞/修复 diff，保存的是受害协议的完整实现代码，用于审计清算与拍卖会计逻辑。

## 已保存内容

### `ajna-core/`（已删除）

Ajna 协议核心（v1.0.0 对照副本）：<https://github.com/ajna-finance/ajna-core>。
原为固定 tag `v1.0.0`（commit `0f59e78031af76d62ad575c18405eb325b28849f`，已用 `git rev-parse v1.0.0^{commit}` 核对一致）的完整 clone。**2026-09-05 按用户要求删除本地副本，只保留漏洞版本 `ajna-v2/`**；如需对照可重新克隆：

```
git clone --filter=blob:none https://github.com/ajna-finance/ajna-core
cd ajna-core && git checkout v1.0.0
```

当时 5 个 submodule 均以 `--depth 1` 浅克隆固定到上游提交（`lib/forge-std` `fc560fa3…`、`lib/openzeppelin-contracts` `d00acef4…`、`lib/prb-math` `e2b59d83…`、`lib/base64` `4d85607b…`、`lib/clones-with-immutable-args` `96f78557…`）；`.gitmodules` 根目录 `base64` 条目为陈旧配置。v1.0.0 世系要点（当时 diff 实证）：rc9（2024-01-04）引入 `COLLATERALIZATION_FACTOR = 1.04`，v1.0.0（2024-02-17）继承；rc1–rc6 与被攻击的部署版一致无此系数。

### `ajna-v2/`

**链上实际被利用版本的完整源码**（媒体称 "Ajna v2"；实为 2023-07 创世部署的 legacy 代码，早于 v1.0.0 tag），取自 Sourcify 验证记录（6 个源码包合并、逐文件哈希零冲突，creation/runtime 均 match）。**行为分析与漏洞复现以本目录为准**（v1.0.0 对照副本 `ajna-core/` 已删除，见上节）。

- 出处、8 个链上合约地址↔角色对照、编译参数：`ajna-v2/PROVENANCE.md`
- 与 v1.0.0 的关键差异：`_isCollateralized` 无 1.04 系数（`src/libraries/helpers/PoolHelper.sol` L158-170）
- 关键文件（建议入口）：`src/libraries/external/TakerActions.sol`（`bucketTake` 奖励/LP 铸造——漏洞本体）、`src/libraries/external/BorrowerActions.sol`（`drawDebt`/五参 `repayDebt`）、`src/libraries/external/SettlerActions.sol`（`settle`）
- 已附 `foundry.toml` remappings；已用 forge 1.8.1 编译并跑通本地全流程 PoC（见下文"PoC 与复现材料"）

链上相关地址（Ethereum，trace 实证）：

- 受害 cbETH/WETH 池：`0xad24FC773e125Edb223C38a39657cB64bc7C178e`（逻辑合约 `0x05bB4F6362B02F17C1A3F2B047A8b23368269A21`，另有 Actions 库 `0x1f172f88…`、`0x51902105…`、`0x39b8bdd2…`、`0xde6c8171…`、`0x33e5c2b4…`）
- 攻击 EOA：`0x6F2f5236b10FE7162Da077A2779f8b5f04b7827e`（战役级另有 `0xc213145e…`、`0xcccc6400…`）
- 攻击主合约：`0x80AD419C4783A09252Ad6a576ce059f51Cc53D47`（入口 selector `0xf1cd0d25`/`0xac00ffb0`；兼作 kicker 与"粉尘抵押借款"仓位）
- 攻击辅助合约：HelperRouter/taker `0xEB0f6A6255d354bc1E314AcCFfe1D0673fa14346`、兑换模块 `0x00c9027573295cE079Aa3b33f2f5c28Ed62c9a77`、鉴权模块 `0x5508df70a2454157A54a27473098716687778542`（`validate(address,address,address)`，攻击方自有 tx.origin 检查，非 Ajna 门禁）
- 被清算 borrower（攻击方自有合约）：`0x02D329Ebb1DA079A89988366b777aF300DB96F5f`
- Setup tx：`0x8a8793963c0ef443b9a396665c3c185ded132d5f99daf7c99e87125597016e64`（block 25854585，约早于攻击 61 分钟）
- Exploit tx：`0x12dfde527ef62882bfabb64362c9ae0e6bfb628363bd298d0d0956c9a114e4f5`（block 25854888，tx index 6）
- 兑换场所：Curve 风格池 `0x5fae7E604FC3e24fd43A72867ceBaC94c65b404A`、UniV3 cbETH/WETH 池 `0x840deeef2f115cf50da625f7368c24af6fe74410` / `0x177622e7…`、UniV3 SwapRouter `0xE592427A…`

## 利用链路与调用栈分析（链上 trace 实证）

> 数据基础：两笔交易的 `debug_traceTransaction`（callTracer + logs）完整调用树、exploit 回执 30 条事件、`prestateTracer`（diffMode）状态差分、攻击前区块（25854887）池状态快照，均经公开归档 RPC 取得并三方对账一致；另有一份调试器级导出（128 帧 / 30 解码事件 / 617 SLOAD / 143 SSTORE）交叉核对吻合。所有数值均可按文中 tx hash 与区块号公开复验；原始数据与脚本已于 2026-09-05 按要求删除，不再留存。
> 版本警示：链上被攻击池是 **2023-07 创世部署的 legacy 代码**（媒体称 "Ajna v2"，实为比 v1.0.0 更老的版本；部署区块实证：逻辑合约 17,622,995 / 2023-07-04，受害池 17,664,706 / 2023-07-10），与 v1.0.0（公开 tag，本地对照副本已删）有已证实差异（部署源码已从 Sourcify 拉取并整理为 **`ajna-v2/`**，详见其 `PROVENANCE.md`）：`repayDebt` 为五参（多 `recipient`）、`bucketInfo` 返回五字段、`_isCollateralized` **无 1.04 系数**（v1.0.0 为 `collateral×LUP ≥ 1.04×debt`，部署版为 `collateral×LUP ≥ debt`——1.04 系 rc9 起新增的加固，非部署版被摘除）、kick 罚金为 3 个月利息。**下文机制与数值一律以部署版源码（`ajna-v2/`）及链上 trace 为准。**

### 0. 总览：setup + exploit 两笔交易

| | Setup tx | Exploit tx |
| --- | --- | --- |
| hash | `0x8a8793…0e64` | `0x12dfde…e4f5` |
| block | 25854585 | 25854888（tx index 6，约 61 分钟后） |
| 作用 | 买抵押品、自抬桶价、造两个仓位并自我 kick | bucketTake 提抵押品、take 结清拍卖、repayDebt 出货 |

### 1. 攻击前池状态（block 25854887 快照，eth_call 实测）

- bucket 2000：quote 存款 49.343733 WETH、LP 49.343733、抵押品 0、汇率 1.004569 —— 全部为攻击者自有存款；该桶价格 ≈ **46,776.65 WETH/cbETH**（市价的约 4 万倍）。
- borrower `0x02D329…`：t0Debt 49.362395 WETH（借款债务 49.3437326 + kick 罚金 0.0187）、抵押品 48.128429 cbETH、npTpRatio 1.026802。
- 其清算拍卖：kicker = 攻击主合约 `0x80AD…`，bondFactor = 1%（下限），bondSize = 0.493437 WETH，kickTime 比 exploit 早约 3,636 秒。
- 拍卖价推算：BucketTake 事件 amount/collateral = 49.343740/1.512187 ≈ **32.63 WETH/cbETH**，与 take 腿 3.474032/0.106465 一致 —— 即 256×referencePrice（≈1.02）起拍、1 小时三次减半后的 32×NP，约为市价 28 倍。**拍卖价并非"衰减趋零"**（此前重构版的关键假设被链上数据证伪）。

### 2. Setup tx（`0x8a8793…`）调用树（trace 摘要）

```
EOA 0x6F2f… → 攻击主合约.ac00ffb0()
├─ 侦察：bucketInfo / depositUpToIndex / borrowerInfo 等静态调用
├─ Balancer Vault.flashLoan(WETH, 105)（费用 0）
│  └─ receiveFlashLoan 回调：
│     ├─ 买入 48.128 cbETH（合计 54.892513 WETH）
│     │   ├─ Curve 池 0x5fae…：exchange 13.030743 WETH → 11.375940 cbETH
│     │   └─ 兑换模块 → UniV3：4.75 WETH → 4.176144 cbETH；37.111770 WETH → 32.577401 cbETH
│     ├─ addQuoteToken(49.343733 WETH → bucket 2000)   ← 自抬桶价 46,776.65；事件 lup=MAX_PRICE(1e9)
│     ├─ drawDebt #1（攻击主合约自己）：押 0.0010548795 cbETH 粉尘、借出 49.319073 WETH
│     │   ※ 部署版检查为 collateral×LUP ≥ debt（无 1.04 系数，Sourcify 部署源码实证）；
│     │     发起费触 5bps 下限 → 债务=借款×1.0005=49.3437326；抵押品精确取 债务/桶价，
│     │     抵押品价值与债务逐 wei 相等 → 合法通过（非绕过，是边界取等）
│     ├─ 转 48.128429 cbETH 给 borrower 合约 0x02D329…
│     ├─ borrower.drawDebt #2：押 48.128429 cbETH、借出 49.319073 WETH（事件 lup=1.025251）
│     │   ※ 抵押品价值=48.128429×1.0252513=49.3437326=债务（逐 wei 取等，合法通过）；
│     │     随后 kick#1 的罚金计入池债务使 LUP 下滑一档，两个仓位水下 → 同块自我 kick 成立。
│     │     （Kick 事件 debt=49.362395 = 借款债务+kick 罚金，罚金=3 个月利息，勿与借款债务混同）
│     ├─ kick #1（攻击主合约的粉尘仓位，bond 0.493437）
│     ├─ kick #2（borrower 的仓位，bond 0.493437）      ← 同一交易内"借款→清算"做局完成
│     └─ 归还闪电贷 105 WETH
└─ 净投入 ≈ 6.6 WETH 种子 + gas；仓位、桶存款、两个拍卖全部就位
```

### 3. Exploit tx（`0x12dfde…`）调用树（trace 摘要）

```
EOA 0x6F2f… → 攻击主合约.f1cd0d25(helper, 1.708e18, 4.0e18+41wei, 48.1284e18, 0.004e18+1, 52.82e18, "")
│
├─ 腿 A（零本金，不用闪电贷）：攻击主合约 → HelperRouter
│  ├─ auctionInfo(borrower) 读拍卖状态
│  ├─ HelperRouter → Pool.bucketTake(borrower=0x02D329…, depositTake=false, index=2000)
│  │   · BucketTake 事件：amount=49.343740 quote（吃空桶 2000 全部自有存款）
│  │       collateral=1.512187 cbETH（按拍卖价 32.63 从拍卖买入）
│  │       bondChange=0.493437、isReward=false ← kicker（=攻击主合约自己）被罚没全部 bond
│  │   · BucketTakeLPAwarded：taker=HelperRouter 获铸 70,685.7 LP，kicker 获 0
│  │       ※ LP ≈ 1.512187 × (46,776.65 − 32.63) —— 奖励按自抬桶价计价，此即 Reward Manipulation
│  ├─ HelperRouter → Pool.removeCollateral(type(uint).max, 2000)
│  │   · 烧掉 70,685.7 LP → 提出 1.511132 cbETH（无赎回时间锁，同交易变现）
│  ├─ Curve 池粉尘兑换（1.5e-12 cbETH ↔ 1.7e-12 WETH，量级可忽略，作用不明）
│  ├─ UniV3 卖出 1.511132 cbETH → 1.719391 WETH
│  └─ HelperRouter → 1.719391 WETH 转账给 EOA                  ← 第一笔落袋
│
├─ 腿 B：Balancer Vault.flashLoan(WETH, 4)（费用 0）
│  └─ receiveFlashLoan 回调：
│     ├─ 再试 bucketTake(borrower, false, 2000) → REVERT（桶已被腿 A 掏空，同一招只能用一次）
│     ├─ Pool.take(borrower, maxAmount, …)
│     │   · Take 事件：付 3.474032 WETH、得 0.106465 cbETH（价格 32.63，溢价部分入池储备）
│     │   · AuctionSettle 事件：剩余 46.509777 cbETH 记回 borrower —— take 内部 _takeLoan→_settleAuction
│     │     顺带结清拍卖，没有独立的 settle() 调用
│     ├─ borrower 合约 → Pool.repayDebt(borrower, 0, 46.509777, recipient=攻击主合约, …)（v2 五参版）
│     │   · RepayDebt 事件：quoteRepaid=0、collateralPulled=46.509777 → cbETH 直达攻击主合约
│     ├─ 兑换模块：exactOutputSingle 卖 2.864871 cbETH → 3.259006 WETH
│     └─ 归还闪电贷 4 WETH
│
└─ 结果：攻击主合约留存 43.751371 cbETH（−0.215 WETH 种子），EOA 留存 1.719391 WETH
```

### 4. 会计勾稽（trace 数值交叉核对）

- 池 cbETH 流出：1.511132（removeCollateral）+ 0.106465（take）+ 46.509777（repayDebt）= 48.127374 ≈ 48.1284（exploit calldata 第 4 参数、borrower 建仓抵押品 48.128429，差值为桶内残留粉尘）。
- 攻击者两笔交易合并：出 54.892513（购 cbETH）+ 49.343733（桶存款）+ 0.986874（两笔 bond）+ 3.474032（take）+ 0.215（种子）≈ 108.9 WETH；入 98.638146（两笔 drawDebt）+ 1.719391 + 3.259006（两笔卖出）≈ 103.6 WETH；留存 43.751371 cbETH ≈ 50 WETH —— 净利 ≈ 44 WETH 量级，与 cbETH 池损失线 $124.8K 吻合。
- 池侧损失：drawDebt #1 的 49.362395 WETH 借款仅有 0.001055 cbETH 粉尘抵押，其拍卖在 exploit tx 中未被处理（最新块查询该拍卖已清空，坏账由 HPB 真实存款豁免承担）+ borrower 仓位抵押品 48.128 cbETH 全部流出 —— 合计约 52 WETH 量级。

### 5. 漏洞机制三段论

1. **自抬桶价（价格体系无预言机）**：向 bucket 2000 存 49.34 WETH，即把该桶价格（46,776.65）挂进池的存款簿；池越浅，单一存款对桶价/LUP 体系的支配越强。
2. **边界取等借款 + 同块自我 kick（边界条件工程化）**：部署版 `_isCollateralized` 为 `collateral×LUP ≥ debt`（无 v1.0.0 的 1.04 系数，Sourcify 部署源码实证）。攻击者把两笔借款的债务（借款额×1.0005，发起费触 5bps 下限）精确做到与"抵押品×自抬/塌陷后的 LUP"逐 wei 相等，合法通过 drawDebt 检查；kick 时池债务已含第二笔借款（LUP 塌到 1.025）且 kick#1 罚金进一步推动 LUP 下滑，两个仓位水下 → 同块自我 kick 成立。kick 罚金（3 个月利息）在 kick 检查之后才计入债务，Kick 事件的 debt 字段含此罚金。
   ※ 更正（2026-09 复盘）：此前所称"v1.0.0 的 1.04 约束下 drawDebt #1 必 revert"**不成立**——LUP 被自抬到 46,776 时，v1.0.0 的 `collateral×LUP ≥ 1.04×debt` 用 0.0011 cbETH（约 $4）粉尘即可满足；同块 draw→kick 在 v1.0.0 下经额外的 LUP 挪动步骤同样可达成。1.04→1.00 的系数变化降低了攻击成本与步骤，但**并非漏洞成立的边界**；漏洞成立的边界是第 1、3 条（桶价可任意挂高 + 奖励按桶价计价），这两条在 v1.0.0 同样存在。
3. **bucketTake 奖励按桶价计价（奖励与成本脱钩）**：taker LP 奖励 ∝ 抵押品 ×（桶价 − 拍卖价），而对手盘只需桶内存款 ≥ 抵押品 × 拍卖价。桶价被自抬 4 万倍后，奖励账面价值被同步放大，且新铸 LP 可立即 `removeCollateral` 变现为拍卖流入桶中的真实抵押品。kicker 罚金按 quote×bpf 计算（此处 1% 下限），与奖励量级完全脱钩 —— 对应 v1.0.0 不变量 **A8**（kicker 奖励 ≤ 借款人罚金）的经济前提失效。

### 6. 对此前"重构版"调用栈的修正（trace 证伪/证实）

1. ~~全部逻辑在闪电贷回调内~~ → 腿 A（bucketTake+removeCollateral+卖出）**先于**闪电贷执行，零本金；闪电贷只服务 take 腿。
2. ~~独立的 `settle()` 调用~~ → 拍卖在 `take` 内部经 `_settleAuction` 顺带结清（Take+AuctionSettle 同帧）。
3. ~~拍卖价衰减趋零~~ → 拍卖价 ≈ 32.63 WETH/cbETH（市价 28 倍）；被抬高的是**桶价**（46,776.65），不是拍卖价压到了 0。
4. ~~Uniswap 单点卖出~~ → 兑换经 Curve 池（setup 中真实量 13.03 WETH）+ UniV3 两个池；exploit 中 Curve 仅粉尘量级。
5. ~~"收割现成闲置拍卖 / 自我做局"两种理论并存~~ → setup tx 实证为**自我做局**：买抵押品→抬桶→双仓位→自我 kick，一笔交易内完成，约 61 分钟后收割。

## PoC 与复现材料

- **本地全流程 PoC（2026-09-10 新增，无需 RPC/fork）**：`ajna-v2/script/AjnaExploit.s.sol`。直接在本目录漏洞版源码上完成"部署 → 做局 → 利用 → 获利与损失转移"全链路证明：以 clone-with-immutable-args 方式部署受害池同款 `ERC20Pool`（forge 自动部署并链接 7 个 Actions 库，clone 参数布局与链上池一致），参数尽量对齐主网：利率取攻击时池内精确值 `1512868055672164`（≈0.1513%，见 `verification/kick_boundary_verification.json` 的 PoolState 解码）、金额逐 wei 镜像 setup tx、等待 3,636 秒。断言结果与主网逐项比对：**A/B 被 kick 后 t0Debt 与主网逐 wei 一致**（49.362395196169210130 / 49.362395197169588347）；拍卖价与主网 32.630709800532780554 仅差 22 wei；bucketTake 铸 LP 与主网 70,685.699662677399190661 仅差 267 wei（kicker 0 LP 一致）；桶残留 4 wei（主网 3 wei）；taker removeCollateral 得 1.511132264828056334 cbETH（主网 …229676，差 1e-7 量级）；二次 bucketTake revert `InsufficientLiquidity`（同链上 F060）；攻击方净利 ≈ **44.8 WETH**、受害 LP 49.344 WETH 存款在 settle 后仅收回 ≈ 4.02（损失 ≈ 45.3 WETH）。残余微量差异全部来自新建池没有受害池 3 年的 inflator 历史（1.000000000 vs 1.000000169），非参数可复现。运行：`cd ajna-v2 && forge script script/AjnaExploit.s.sol:AjnaExploitScript -vvv`（实测通过，forge 1.8.1 / solc 0.8.18）。

- **主网逐 wei 精确重放（2026-09-10 新增，无需 RPC/fork）**：`ajna-v2/script/AjnaExploitExactReplay.s.sol`。部署同一漏洞版实现后，用 `vm.store` 把 `verification/raw/exploit_prestate_full.json` 中 exploit tx 实际访问的 85 个池存储槽（= 25,854,887 区块末前态）直接移植进本地池（生成器：`verification/generate_prestate_sol.py` → `script/generated/ExploitPreState.sol`），再以主网地址与参数执行 exploit 四腿。断言全部**逐 wei 等于**链上值（`verification/decoded_evidence.json`）：BucketTake amount 49.343739875664121569 / collateral 1.512187144481253596 / bondChange 0.493437325579859365 / isReward=false；BucketTakeLPAwarded taker 70,685.699662677399190661、kicker 0；removeCollateral 1.511132264828229676；桶残留 3 wei；take 3.474032198249838476 → 0.106465112756852011 cbETH 并结清拍卖；repayDebt 零 quote 提回 46.509777147197339148 cbETH（lup=99,836,282,890）；终态池 WETH 4.510510701313692626、池 cbETH 0.658157103070465363、A 持有 46.616242259954191159 cbETH、A 坏账与拍卖原样保留。运行：`cd ajna-v2 && forge script script/AjnaExploitExactReplay.s.sol:AjnaExploitExactReplay -vvv`（实测通过）。与上一条约有机全流程脚本互补：前者证明"从部署到利用"的机制可复现，本条证明 exploit 输出与主网逐 wei 一致。
- DeFiHackLabs PoC 源码（可在线阅读）：<https://github.com/SunWeb3Sec/DeFiHackLabs/blob/main/src/test/2026-08/AjnaFinance_exp.sol>。其复现方式是 fork 到攻击前区块（25854887），把链上原始 196 字节 calldata 原样重放给已部署的攻击合约 `0x80AD…`（`prank` 成攻击 EOA 使其自有的 tx.origin 鉴权通过），并非用 Solidity 重写攻击逻辑。该 calldata 已解码核对（见"利用链路与调用栈分析"第 3 节的参数）。
- 如需自行跑 PoC：克隆 DeFiHackLabs 后 `forge test --contracts ./src/test/2026-08/AjnaFinance_exp.sol -vvv`（需主网归档 RPC）。
- 链上数值核对结论（原始数据已删，可按 tx hash 公开复验）：池 cbETH −48.127374525 = 1.511132265（removeCollateral）+ 0.106465113（take 所得）+ 46.509777147（repayDebt 拉走）；攻击主合约 cbETH 0→43.751371389；EOA WETH 0→1.719390871；LP 铸造/烧毁同额 70,685.699663；池入口四个 selector 全部解码为部署版接口函数；池 41 个 storage 槽终值与 prestateTracer 差分逐槽一致。调试器级导出另增补五处细节：①腿A 先经 Curve 风格池做粉尘兑换（1,511,132 wei cbETH→1,720,317 wei WETH）再走 UniV3，EOA 实收为两笔之和 1.719390871405544952；②主合约第二笔 `bucketTake` 因桶 2000 流动性已被首笔抽空而 revert（`InsufficientLiquidity()`），随后退化为 `take`；③闪贷额为 4e18+41 wei（Balancer 零费率）；④`RepayDebt` 事件 `lup = 99,836,282,890`（≈1e-10 WETH，钉在 MIN_PRICE 附近）；⑤`BucketTakeLPAwarded`：taker 独得 70,685.699663 LP、**kicker 为 0**——奖励操纵的直接证据。
- 本地全流程复现（不需要 RPC）：`cd ajna-v2 && forge script script/AjnaExploit.s.sol:AjnaExploitScript -vvv`，从部署漏洞版合约到利用、获利与受害 LP 损失转移一次跑通（2026-09-10 实测通过，详见上文新增条目）。

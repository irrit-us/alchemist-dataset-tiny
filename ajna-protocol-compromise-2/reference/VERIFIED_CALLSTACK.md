# Ajna 链上验证与受验证调用栈

验证日期：2026-09-08。验证范围为 cbETH/WETH 实例的 setup 与 exploit 两笔已发生交易。数据来自无需登录或 API key 的公开 RPC 与 Sourcify；所有查询均为只读。

**验证结论：两笔交易的 272 个 EVM 调用帧及 60 条回执事件支持此前的主要利用链路；本次同时纠正第二次 bucketTake 的布尔参数、桶的粉尘余量、LP 汇率字段与精确损益口径。**

**1. 证据来源、身份锚点与验证强度**

| 项目 | Setup | Exploit |
| --- | --- | --- |
| 交易 | [浏览器](https://etherscan.io/tx/0x8a8793963c0ef443b9a396665c3c185ded132d5f99daf7c99e87125597016e64) | [浏览器](https://etherscan.io/tx/0x12dfde527ef62882bfabb64362c9ae0e6bfb628363bd298d0d0956c9a114e4f5) |
| 区块 / 交易索引 | 25,854,585 / 63 | 25,854,888 / 6 |
| UTC | 2026-08-28T15:18:35+00:00 | 2026-08-28T16:19:11+00:00 |
| 状态 | 0x1，成功 | 0x1，成功 |
| callTracer 帧数 | 145 | 127 |
| 回执事件数 | 30 | 30 |
| 池发生变化的 storage 槽 | 39 | 41 |
| Gas used | 2,635,305 | 1,384,486 |
| 实付 gas（ETH） | 0.00463849502754987 | 0.00344442716579952 |

完整区块哈希：
```text
setup:   0xd4fda30c923b5f5c90c3abcb430f51202ccccb49d67ae99802217e9acdf9c71d
exploit: 0x3d1b92a6d9c2f56c909de75b28f0ae6cc26acf4f3f91f6d8244b50c2e4398757
```

PublicNode、dRPC、1RPC 返回的 exploit 回执在区块哈希、状态、gas、交易标识和所有事件上相同。dRPC 提供两笔完整 callTracer、prestateTracer（完整前态及 diffMode）；历史 eth_call 提供三个区块末状态。交易级差分用于 token 余额验证，避免把同区块其他交易造成的变化混入本交易。

来源是公开节点返回的历史执行结果，并非本地独立重放或自建全节点证明；三个公开域名也不保证其底层基础设施彼此独立。callTracer 的调用层次仍主要依赖 dRPC，回执与源码提供独立的交叉核对。

本次自动核验共 **47/47 项通过**，包括来源一致性、日志内容及顺序、运行时代码、源码哈希、token 存储差分、抵押品守恒和拍卖价格公式。详见 [解码与来源核验](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/verification/decoded_evidence.json>)、[会计核验](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/verification/accounting_verification.json>)。

trace 服务对日志编号的返回口径存在差别：setup 的 index 为交易内 0–29，对应回执全区块 logIndex 121–150，统一偏移 +121；exploit 已返回区块全局编号，偏移为 0。保留原始数据，先核对 address/topics/data，再检查统一偏移后的完整顺序；没有把事件重排成预期链路。

**2. 实际部署版本已重新验证**

- 受害池在区块 17,664,705 的 eth_getCode 返回 0x，在 17,664,706 首次非空；该代码与攻击前区块一致。对应 2023 年 7 月部署。
- 逻辑合约在区块 17,622,994 无代码，17,622,995 有代码；攻击前运行时代码与 Sourcify 返回的链上代码逐字节相同。
- 受害池 clone 字节码包含预期逻辑地址、cbETH 地址和 WETH 地址；trace 又实际进入该逻辑及链接库。
- Sourcify 元数据覆盖本地 **49 个唯一源码文件**，共 219 次逐文件 keccak256 比较全部一致；两笔交易前态中取得的 10 个合约代码实例与 Sourcify runtime 对齐。
- Sourcify 状态为 match；本文不将其改称 exact_match，也未声称本次自行重新编译。

[Sourcify 逻辑合约](https://repo.sourcify.dev/1/0x05bB4F6362B02F17C1A3F2B047A8b23368269A21)、[Sourcify API 说明](https://docs.sourcify.dev/blog/apiv2-lookup-endpoints/)。

**3. 受验证调用栈：setup**

帧号 F000 起，按 callTracer 树先序遍历；每个完整调用栈文件还保留原树 path、调用类型、from/to、gas、解码参数与返回值。以下仅列关键帧，CALL → DELEGATECALL 表示同一次业务操作的执行层次，不能重复计算金额。

```text
F000 EOA → AttackerMain/A：0xac00ffb0（未验证源码的入口，保留 selector）
└─ F026 → BalancerVault.flashLoan(WETH, 105000000000000000003 wei)
   └─ F030 → AttackerMain.receiveFlashLoan(..., feeAmounts=[0], ...)
      ├─ 兑换取得 cbETH
      ├─ F098 → Pool.addQuoteToken(49.343732556986936488 WETH, 2000, ...)
      │  └─ F099 → ERC20Pool → F100 LenderActions.addQuoteToken
      ├─ F103 → Pool.drawDebt(A, 49.319073020475698638 WETH, 7388,
      │                       0.001054879496563856 cbETH)
      │  └─ F104 → ERC20Pool → F106 BorrowerActions.drawDebt
      ├─ F114 → Pool.drawDebt(B, 49.319073021475198888 WETH, 7388,
      │                       48.128429404435444755 cbETH)
      │  └─ F115 → ERC20Pool → F117 BorrowerActions.drawDebt
      ├─ F127 → Pool.kick(A, 7388)
      │  └─ F128 → ERC20Pool → F129 KickerActions.kick
      ├─ F132 → Pool.kick(B, 7388)
      │  └─ F133 → ERC20Pool → F134 KickerActions.kick
      └─ 归还本笔 flash loan
```

完整数据：[setup 全部 145 帧](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/verification/setup_callstack.md>)；[原始 callTracer 响应](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/verification/raw/drpc_setup_calltrace.json>)。两次借款金额相差 999,500,250 wei，并非逐 wei 相同。

**4. 受验证调用栈：exploit**

```text
F000 EOA → AttackerMain/A：0xf1cd0d25（保留未知入口 selector）
├─ F002 → Pool.auctionInfo(B)：读取 kickTime、NP、bond 等
├─ F004 → Helper/Taker
│  ├─ F009 → Pool.bucketTake(B, false, 2000)
│  │  └─ F010 → ERC20Pool → F012 TakerActions.bucketTake
│  │     ├─ logIndex 73：taker 获 70685.699662677399190661 LP
│  │     └─ logIndex 74：用 49.343739875664121569 WETH 债权
│  │                       取得 1.512187144481253596 cbETH 入桶
│  ├─ F014 → Pool.removeCollateral(MAX_UINT, 2000)
│  │  └─ F015 → ERC20Pool → LenderActions
│  │     logIndex 75：提 1.511132264828229676 cbETH，烧同额奖励 LP
│  └─ 兑换并转给 EOA：1.719390871405544952 WETH
└─ F054 → BalancerVault.flashLoan(WETH, 4000000000000000041 wei)
   └─ F058 → AttackerMain.receiveFlashLoan(..., feeAmounts=[0], ...)
      ├─ F060 → Pool.bucketTake(B, true, 2000)
      │  └─ F061 → ERC20Pool → F062 TakerActions
      │     REVERT 0xbb55fd27 = InsufficientLiquidity()
      ├─ F063 → Pool.borrowerInfo(B)：残余 t0Debt 尚未清零
      ├─ F068 → Pool.take(B, MAX_UINT, AttackerMain, 0x)
      │  └─ F069 → ERC20Pool → F070 TakerActions.take
      │     ├─ logIndex 89：付 3.474032198249838476 WETH
      │     │               取 0.106465112756852011 cbETH
      │     └─ logIndex 90：AuctionSettle，剩余 46.509777147197339148 cbETH
      ├─ F079 → Pool.borrowerInfo(B)：t0Debt=0，抵押品仍在
      ├─ F084 → Pool.repayDebt(B, 0, 46.509777147197339148 cbETH, Main, 7388)
      │  └─ F085 → ERC20Pool → F086 BorrowerActions.repayDebt
      │     logIndex 93：quoteRepaid=0，collateralPulled=46.509777147197339148
      ├─ F090 → Pool.borrowerInfo(B)：t0Debt=0，collateral=0
      ├─ F092/F094 → auctionInfo(A)/borrowerInfo(A)：粉尘债务及拍卖仍在
      └─ 兑换部分 cbETH，归还本笔 flash loan
```

完整数据：[exploit 全部 127 帧](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/verification/exploit_callstack.md>)；[原始 callTracer 响应](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/verification/raw/drpc_exploit_calltrace.json>)。F060 的失败被上层处理，整笔交易成功。失败在 Pool、实现与库三个帧传播，属于一次失败操作。

外部库带 storage 参数的入口通常不出现在常规 ABI function 列表中。本次额外对 Sourcify 编译器 devdoc 中的库函数完整签名做 keccak256，确认 bucketTake 的 0x2f39ec5c、take 的 0x0f4a0c2d、repayDebt 的 0x9883470d 等；库的 storage 指针及结构体 calldata 保留原值，不伪装成普通 ABI 参数。内部 _rewardBucketTake / _settleAuction 不形成独立 EVM 调用帧，其执行位置由对应外部库帧的事件与源码关联。

**5. 状态、公式和会计交叉验证**

补充解码 setup F129/F134 的 KickResult 和 PoolState：A kick 前池债务为 98.687465114971872974 WETH，全部存款为 98.687749844521015658 WETH；A kick 后债务为 98.706127754155146617 WETH，已超过存款。F129 返回 LUP=MIN_PRICE=0.000000099836282890，F134 的输入池债务与该输出一致。B 按此 LUP 的抵押价值只有 0.000004804963493073 WETH，而当时债务为 49.343732557985936487 WETH，所以可以 kick。旧摘要所谓‘下降一档’不准确。新增原始字段解码及断言见 [kick 边界核验](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/verification/kick_boundary_verification.json>)，由 verify_kick_boundary.py 独立生成。

| 核验对象 | 攻击前 | 攻击后 |
| --- | --- | --- |
| B：t0Debt | 49.362395197169588347 | 0 |
| B：cbETH 抵押品 | 48.128429404435444755 | 0 |
| A：t0Debt | 49.362395196169210130 | 相同，未清偿 |
| A：cbETH 抵押品 | 0.001054879496563856 | 相同 |
| 桶 2000：quote deposit | 49.343732556986936488 WETH | **3 wei WETH** |
| 桶 2000：抵押品 | 0 | 0.001054879653023920 cbETH |
| 桶 2000：LP | 49.343732556986936488 | 相同：奖励 LP 铸造后全部烧回 |
| 桶 2000：真正 LP exchange rate | 1 | 1.000000148320299802 |

这里 borrowerInfo 第一项是 t0Debt，必须乘 inflator 才是应计债务。交易后 inflator=1.000000174428866379，debtInfo 返回仅剩 A 的应计池债务约 49.362403806395845950 WETH。bucketInfo 第五项是 scale，攻击前为 1.004568828197116541；独立调用 bucketExchangeRate(2000) 才得到 LP 汇率 1。

攻击相隔 3,636 秒。NP=1.026802322998020354，kickMomp=1.025251253128124958：
```text
32 × max(kickMomp, NP) × 2^(-(3636/3600 - 1))
= 32.6307098005327805549592821111578299921399709090558466958368 WETH/cbETH
BucketTake.amount / BucketTake.collateral
= 32.6307098005327805759081077282093810673501167659731394432193 WETH/cbETH
```

两者误差约 2.1×10^-17 WETH/cbETH，符合定点计算及抵押品取整误差。由此验证的是本部署版 32 倍、首小时锁价公式。

逐 wei 抵押品守恒：
```text
48128429404435444755
= 1512187144481253596  (bucketTake)
+ 106465112756852011   (take)
+ 46509777147197339148 (repayDebt 提回)

1512187144481253596 - 1511132264828229676
= 1054879653023920     (桶内残留 cbETH)
```

**6. token 净流与存储差分**

下表是两笔交易分别取 Transfer 净额后求和，不含其他未检查交易。已用 prestateTracer 的交易前后 token storage 值核对相关非零余额变化；WETH balance mapping 在槽 3，cbETH 在槽 9，具体 keccak 槽地址及整数前后值存于 accounting_verification.json。

| 对象 | 两笔合计 WETH 变化 | 两笔合计 cbETH 变化 |
| --- | ---: | ---: |
| 攻击方地址组 | -5.080609128594455048 | 43.751371388571168932 |
| 受害池 | -44.833506635564403832 | 0.002109759149587776 |

两笔 gas 合计 **0.00808292219334939 ETH**，与 EOA 原生 ETH 余额下降相符。攻击方地址组包括 EOA、Main、Helper、B 与兑换模块；后续未检查的交易、未领取保证金及残留 LP 不计入表内。

这是已验证的资产数量变化，不能直接称为美元净利润。若将剩余 cbETH 按同一时点价格 p（WETH/cbETH）计价，两笔已检查交易的简化持仓收益为：
```text
43.751371388571168932 × p - 5.080609128594455048 - 0.00808292219334939
（以 WETH/ETH 1:1 计 gas；未计未结权益及未来卖出成本）
```

exploit 单笔池 cbETH 从 48.785531627852886198 降至 0.658157103070465363；池 WETH 从 1.036478503063854150 增至 4.510510701313692626。两笔合并池仍净流出 WETH，是因为 setup 已借走资金。B 的抵押品回收和 A 的坏账是同一资产负债变化的不同侧面，不能相加计算损失。

**7. 本次确认、更正与未覆盖事项**

- 确认：先 kick A 后 kick B；先 bucketTake(false)，后 bucketTake(true) 失败，再 take 与零 quote 的 repayDebt；A 的贷款和拍卖在本笔末尾仍存在。
- 更正：高价桶剩余 3 wei quote，不能写成严格清零。它远不足以按高桶价买入 1 wei cbETH，与 InsufficientLiquidity 回滚相符；本文未额外获取 opcode trace 来定位此次 revert 的 PC。
- 更正：bucketInfo 第五项不是 LP exchange rate；borrowerInfo 第一项是 t0Debt，而非自动包含最新利息的债务。
- 更正：当前 callTracer 返回 145/127 帧。旧归档所谓 128 帧来自不同工具口径，未证明与本次计数等价。
- 已验证区块末 A 仍有坏账风险；本次没有追踪其后最终 settle 的交易，因而“最终由哪个具体桶承担多少损失”仍不作为已完成的链上验证。
- 七池战役总额约 77.5 万美元仍为外部报告口径；本次仅核验 cbETH/WETH 两笔交易，不推广为全部池的独立验证。

**8. 可复验文件**

- [原始文件 SHA-256 清单](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/verification/manifest.json>)：原始请求、返回及 Sourcify 数据。
- [解码证据](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/verification/decoded_evidence.json>)：帧路径、输入、输出、错误、事件及来源检查。
- [会计与状态验证](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/verification/accounting_verification.json>)：历史状态、slot 级余额差、公式检查与被证伪的旧说法。
- [采集及重验说明](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/verification/README.md>)：公开接口、依赖和执行命令。

[Geth callTracer/prestateTracer 文档](https://geth.ethereum.org/docs/developers/evm-tracing/built-in-tracers)说明两类输出的语义。此报告保留未知攻击方入口的 selector，不用未验证的函数名填补调用栈。

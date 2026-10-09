# Ajna 根因位置与影响范围边界

补充日期：2026-09-08。历史利用仍以已验证的 cbETH/WETH 池为对象；新增对照是公开仓库 v1.0.0 的固定提交 `0f59e78031af76d62ad575c18405eb325b28849f`。未指定、未验证任何“新池”的链上地址，因此不能把公开源码差异直接视为某个现存池的安全证明。

**根因定位**

关键组合是 `TakerActions.bucketTake → _takeBucket → _calculateTakeFlowsAndBondChange → _rewardBucketTake`：池以尚未承担坏账的桶存款账面金额计算清算可支付金额，注销另一 borrower 的债务；高于市场的拍卖价使债务可以仅用少量抵押品偿清，极高桶价对应的 LP 奖励又让 taker 回收几乎全部转入桶的抵押品。随后 B 无债务提回剩余抵押品，是该会计结果允许的正常行为。

| 代码位置（实际部署版） | 执行的动作 | 在本次组合中的作用 |
| --- | --- | --- |
| [PoolHelper.sol:164](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/ajna-v2/src/libraries/helpers/PoolHelper.sol:164>) | `C × LUP ≥ D` | 自选高价桶支持 A 的粉尘借款 |
| [TakerActions.sol:431](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/ajna-v2/src/libraries/external/TakerActions.sol:431>) | 读取桶 deposit；要求拍卖价不高于桶价 | 桶价、拍卖价均高于市场时仍可通过 |
| [TakerActions.sol:749](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/ajna-v2/src/libraries/external/TakerActions.sol:749>) | `quoteTokenAmount = unscaledDeposit × bucketScale` | 以账面债权面值确定购买能力 |
| [TakerActions.sol:755](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/ajna-v2/src/libraries/external/TakerActions.sol:755>) | `collateralAmount = quote / borrowerPrice`；据此计算 `t0RepayAmount` | 高拍卖价让少量抵押品对应大额债务注销 |
| [TakerActions.sol:168](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/ajna-v2/src/libraries/external/TakerActions.sol:168>) | 从目标 borrower 扣减应偿债务 | B 的实际债务下降 |
| [TakerActions.sol:624](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/ajna-v2/src/libraries/external/TakerActions.sol:624>) | 按 `collateral × (bucketPrice−auctionPrice)` 铸 LP | 将桶内新增抵押品的绝大多数权益分给 taker |
| [TakerActions.sol:662](<C:/Users/Jesse/Desktop/ExpAnalystic/9-2/Ajna Protocol Compromise 2/ajna-v2/src/libraries/external/TakerActions.sol:662>) | 消耗桶 quote deposit | A 坏账核销前，高价桶原本应承担损失的 quote 存款已几乎耗尽 |

上述存款抵债与价差奖励在正常场景各有用途；仅看某一算术表达式并不存在必然溢出或必然凭空增发现金。漏洞评价应覆盖整池可回收资产及坏账承担顺序，而不能只验证一次调用内借贷记账是否配平。我先前将“LP 奖励公式”单独称作漏洞本体过于简化。

**公开新版差异能证明什么**

实际下载的对照源码保存在 `verification/version_comparison/`，URL、固定提交和 SHA-256 见其 `PROVENANCE.json`。它不是已验证的新池部署源码。

| 差异 | 对本次链路的可确认影响 | 不能据此推出 |
| --- | --- | --- |
| v1.0.0 `_isCollateralized` 引入 1.04 系数 | 原样 A 的抵押估值约 49.3437，所需估值约 51.3175 WETH，检查失败 | 所有调整后的组合均不可利用 |
| 同函数增加 MIN_PRICE 且有债务时返回 false | 防止底价下仍被认作足额抵押 | 阻止本次零债务 B 提款；零债务不在该限制内 |
| 清算收费、BPF 参考值、价款与偿债额计算改变 | 旧版精确金额及获利模型不可直接套用 | 无需整体验证即可认定修复 |
| 拍卖曲线变更，`AuctionNotTakeable` 禁止同块 take | 改变交易时序与报价 | 直接挡住本次已等待 3,636 秒的 take |
| `_rewardBucketTake` 仍有同一价差奖励表达式 | 新版没有简单删除该机制 | 仅凭公式仍存在就断言新版一定可利用 |

官方对照：[抵押检查](https://github.com/ajna-finance/ajna-core/blob/0f59e78031af76d62ad575c18405eb325b28849f/src/libraries/helpers/PoolHelper.sol#L213)、[清算与奖励](https://github.com/ajna-finance/ajna-core/blob/0f59e78031af76d62ad575c18405eb325b28849f/src/libraries/external/TakerActions.sol#L603)。

本次只做源码比较和同输入抵押条件的整数核算，没有在新版上运行完整攻击重放或经济不变量测试。“原样输入失败”与“新版所有池安全”不是同一个结论。

**为什么不能说其他池都不受影响**

**补充：v1.0.0 是否即时核销坏账（源码验证）**

没有发现“kick 后立即按潜在损失扣减桶存款，bucketTake 前先核销其他 borrower 坏账”的机制。应区分拍卖债务记录、提款限制与实际损失分摊。这里的桶存款债权是 bucketTake 的抵债来源，并非 borrower 质押的抵押物；本案的借款抵押物仍是 cbETH。

- `verification/version_comparison/Pool.sol:315` 在 kick 后增加 `t0DebtInAuction`；`KickerActions.sol:307` 的 `_kick` 不接收 deposits，也不扣减桶存款。其 `t0ReserveSettleAmount` 是后续结算使用准备金的额度记录，并非当场核销。
- `RevertsHelper.sol:36` 按拍卖债务从最高价桶向下锁定相关存款，`Pool.sol:235`、`:239` 在提取 quote 前检查可结算拍卖与存款锁定。这是提款限制，不是账面存款减值；可结算拍卖检查只检查队首。
- `ERC20Pool.sol:429` 的 bucketTake 入口计息后直接调用 TakerActions，没有先调用 settle；`TakerActions.sol:431`、`:442` 读取目标桶的 unscaledDeposit 与 scale。没有先按 A 的潜在回收缺口折价这一桶存款。
- `SettlerActions.sol:113` 要求拍卖超过 72 小时，或该 borrower 的抵押物已为零，才允许 settle。之后先以高价桶存款接收剩余抵押品；抵押品耗尽仍有债务时，再按规则使用准备金，并由 `_forgiveBadDebt` 分摊剩余坏账。`:485`、`:494` 的 `Deposits.unscaledRemove` 才实际扣掉用于核销的桶存款。结算还有 bucketDepth 上限，不保证一次调用清完全部债务。

因此，不能声称新版安全是因为“坏账即时同步，受损债权不能再参与 bucketTake”。但这也不能反推出新版一定可利用：v1.0.0 的 kick 不再沿用本案旧版的 kick 加债路径，抵押检查和清算价款计算等也不同；原样利用失败与完整安全证明仍需区分。此处是固定提交的静态代码核查，没有新增的新版链上调用栈或完整重放。

链上已验证的低成本前置条件是：受害池原贷款债务为 0，但有他人的真实 quote 存款；攻击者增加一个高价桶后，其新增贷款单独就能由该桶覆盖，因此 LUP 被推到该高价档。

一般而言，要让 LUP 留在某高价档，必须满足：

```text
该档及更高档累计存款 ≥ 原池总债务 + 新增债务
```

其他池若已有债务、存款分布不同，攻击者对 LUP 的控制成本会不同；若可借现金很少、市场兑换滑点大、费用或清算成本较高，也可能无法按本样本获得正收益。这些是代码和经济模型推导的必要评估维度，并非已逐池验证的免责条件。

池的借款、存款桶和坏账账本各自独立。一个池的损失不会通过本次代码直接核销另一池的存款；但共享有问题实现的多个池仍可能被分别攻击。因此应区分“未被这次交易波及”“未见公开攻击”“已证明不受同类问题影响”。

“新池”也要按工厂和实际实现地址区分，而不能只看创建日期：通过旧工厂新建的池仍可能使用旧代码。对一个具体池的影响判断，需要其攻击时实现/库地址、验证源码、存款分布、债务与现金状态，以及完整偿付能力验证；目前没有足够证据给所有未列入攻击名单的池下安全结论。

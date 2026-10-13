# 邀请码与自动维护

## 替换推广链接

所有推广入口集中在 `config/affiliate-links.json`。键是机场ID，空字符串使用官方无邀请码入口。

```json
{
  "boostnet": "https://你的官方域名/register?code=你的邀请码"
}
```

只修改相应键，保留其他机场键。使用你在官方后台取得的完整推广URL，不机械拼接不同面板的参数。当前默认配置全部为空，没有保留参考作者邀请码。推广入口与资料查询的官方入口分别显示，避免邀请参数污染巡检。

```bash
python3 scripts/catalog.py validate
python3 scripts/catalog.py generate
python3 -m unittest discover -s tests -v
git add config README.md docs providers reports
git commit -m 'docs: configure referral links'
git push
```

## 修改机场资料

单一来源为 `data/<id>.json`。每个套餐单独记录价格、币种、付费月数、流量、重置方式、节点倍率、手续费、来源与核验日。不限时包 billing_months=null；全年共用 reset=total；monthly 的 billing_months 必须为正整数。

- verified_at=null：社区参考，仍可能过期。
- verified_at=官网核验日期：公开套餐已核验，90天后退出已核验榜。
- status=unverified：尚无本仓库实测。
- status=active：有运营实测依据；不能仅靠网页200标记。
- status=watch / inactive：排除所有价格排行，保留详情和历史资料。
- mirrors：维护者确认的其他官方HTTPS入口，自动巡检。
- regions / device_limit：取得证据后填入；未知不猜测。

每个字段沿用该条目 sources 的记录；若字段取自新的来源，先补 `config/sources.json` 和对应套餐 source。促销先作为 notes 记录，核对适用套餐和期限后再计算真实支付额。

## 实测综合评分

quality 默认 null。录入前完成真实测试，并将公开证据链接到自有记录或可信公开报告：

```json
{
  "tested_at": "2026-10-13",
  "network": "电信1000M家宽",
  "region": "广东",
  "evidence": "https://github.com/你的账号/你的仓库/issues/真实测试记录号",
  "stability": 85,
  "speed": 80,
  "unlock": 70,
  "support": 80
}
```

各项0–100：稳定性记录测试次数、成功率、晚高峰丢包；速度记录多节点多时段中位数与本地基线；解锁记录自己测试目标的成功比例；客服记录响应时间与实际解决结果。分数必须能从证据解释，不从线路名称、运营年限或推广佣金推算。建议至少7天观察，同地区同运营商对比。权重在 config/ranking.json，默认40/25/15/20。价格榜单独显示，避免质量分与流量成本互相掩盖。

## 自动化范围

| 工作 | 周期 | 行为 |
| --- | --- | --- |
| 数据完整性、排名回归、生成文件一致性 | push / PR | CI验证 |
| 官方与镜像入口检查 | 每天北京时间10:17 | 公开HTTPS访问，生成健康报告 |
| 社区原文和官方来源变更 | 每日 | SHA256比较，正文变化进入待办 |
| 套餐过期提醒 | 每日 | 超90天或未核验的套餐进入核验列表 |
| 待办提醒 | 发现内容变化时 | 创建或更新同一个“自动维护待办”Issue |
| 派生页面与巡检报告 | 每日 | 机器人提交到main；不改来源JSON与邀请码 |

Actions → Daily public link maintenance → Run workflow 可手动执行。首次建立内容基线；后续变更保留提醒，维护者复核后将 reports/health.json 中 baseline_sha256 设置为本次 sha256。反爬403/429标记restricted；超时和DNS标记unknown，不直接下结论。

需要 GitHub Actions 启用且工作流具有 contents:write、issues:write。无需付费API、PAT或服务器。若main有保护规则，机器人直接push会被拒绝，此时改为你自己的审查/PR策略；不绕过保护。定时任务可能延迟，公开仓库长期无活动可能暂停，参见 [GitHub官方定时工作流说明](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)。

自动化不登录机场后台，不付款，不访问个人订阅，不推测节点质量，不自动抓取他人的推广码。价格、优惠和线路调整由维护者核对官网后更新，机器人负责线索与报告。

## 导出和本地查询

```bash
python3 scripts/catalog.py search --query TAG
python3 scripts/catalog.py search --protocol AnyTLS --reset total
python3 scripts/catalog.py search --route 直连 --max-monthly 20 --currency CNY
python3 scripts/monitor.py
python3 scripts/catalog.py generate
```

程序只依赖Python标准库。JSON/CSV在reports，Markdown在providers和docs。不需要本地服务或额外部署。

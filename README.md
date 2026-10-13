# 机场资料库 · 套餐对比与性价比排行

[![检查](https://github.com/luluarthub/airport-guide/actions/workflows/ci.yml/badge.svg)](https://github.com/luluarthub/airport-guide/actions/workflows/ci.yml)

收录 **29 家服务、71 个套餐**。覆盖专线、中转、直连、低价、全年流量包和不限时套餐。资料按来源整理，未亲测条目明确标记。

## 快速入口

- [全部机场与信息查询](docs/catalog.md)
- [性价比排行：已核验 / 参考 / 综合](docs/rankings.md)
- [免费与试用入口](docs/trials.md)
- [购前检查与场景选择](docs/buying.md)
- [客户端与使用入门](docs/clients.md)
- [故障排查与常见问题](docs/faq.md)
- [入口检查与来源变更报告](reports/health.md)
- [邀请码替换与自动维护](docs/maintenance.md)
- [来源与数据说明](docs/sources.md)

## 按需求查找

GitHub 页面内可使用浏览器搜索；每家都有独立资料页。需要多条件筛选可下载仓库后运行：

```bash
python3 scripts/catalog.py search --query 海獭
python3 scripts/catalog.py search --route 直连 --max-monthly 20 --currency CNY
python3 scripts/catalog.py search --protocol AnyTLS --reset total
```

预算筛选按折合月费，全年共用与不限时包单独标识；真实支付金额见详情。下载 [JSON](reports/catalog.json) 或 [CSV](reports/plans.csv) 可在表格中筛选全部套餐。

## 机场概览

| 机场 | 线路 | 资料 |
| --- | --- | --- |
| 365VPN | 官方客户端 | [查看](providers/365vpn.md) |
| 贝贝云 | 海外中转 | [查看](providers/beibei.md) |
| BoostNet | 专线 / 透传 | [查看](providers/boostnet.md) |
| 次元雲 | 中转 | [查看](providers/ciyy.md) |
| E-IX | 透传专线 | [查看](providers/eix.md) |
| FlyBit | 中转 | [查看](providers/flybit.md) |
| 飞喵云 | 中转 | [查看](providers/fmyun.md) |
| 自由猫 | 中转 | [查看](providers/freecat.md) |
| 蜂窝云 | 中转 | [查看](providers/fwcloud.md) |
| 海獭 | 中转 / 透传 | [查看](providers/haita.md) |
| happy猫 | 中转 | [查看](providers/happymao.md) |
| iNetS | 直连 优化 | [查看](providers/inets.md) |
| Just My Socks | 直连 | [查看](providers/jms.md) |
| Kycloud | 专线 / 海外中转 | [查看](providers/kycloud.md) |
| 老猫云 | 海外中转 | [查看](providers/laomao.md) |
| 良心云 | 直连 | [查看](providers/liangxin.md) |
| M78星云 | 中转 | [查看](providers/m78star.md) |
| 农夫山泉 | 中转 | [查看](providers/nfsq.md) |
| 念云 | 直连 优化 | [查看](providers/nianyun.md) |
| NyanSS | 中转 | [查看](providers/nyanss.md) |
| ofoNET | 中转 | [查看](providers/ofonet.md) |
| 壹速云 | 中转 | [查看](providers/onesy.md) |
| 赔钱机场 | 直连 | [查看](providers/peiqian.md) |
| 山海 | 直连 / 中转 | [查看](providers/shanhai.md) |
| TAG | 专线 | [查看](providers/tag.md) |
| 兔兔云 | 中转 | [查看](providers/tutuyun.md) |
| WgetCloud | 专线 | [查看](providers/wgetcloud.md) |
| 一分机场 | 直连 | [查看](providers/yifen.md) |
| 悠兔 | 专线 / 中转 | [查看](providers/youtu.md) |

## 透明原则

价格按来源和核验日期公开；参考数据不冒充实测。推广链接不参与评分，默认全部使用无邀请码的入口，配置后可能包含推广收益。榜单按币种、重置方式分组，不通过猜测汇率混排。

仅检查公开网站，不公开用户订阅、节点凭据或账号信息。速度与解锁需要有日期、地区和运营商的测试证据。建议先短期验证自己的网络体验。

## 更新与贡献

每天北京时间 10:17 自动检查入口和参考来源，生成报告；每次提交自动校验数据和页面。资料修改用 JSON 单一来源，避免 README 与详情互相矛盾。参见 [维护说明](docs/maintenance.md) 和 [贡献流程](CONTRIBUTING.md)。

代码采用 MIT；社区参考仓库文章、截图与品牌标识未复制，相关权利归原作者。

# 机场资料库 · 套餐对比与性价比排行

[![检查](https://github.com/luluarthub/airport-guide/actions/workflows/ci.yml/badge.svg)](https://github.com/luluarthub/airport-guide/actions/workflows/ci.yml)

收录 **93 家服务、80 个套餐**。覆盖专线、中转、直连、低价、全年流量包和不限时套餐。资料按来源整理，未亲测条目明确标记。

## 快速入口

- [全部机场与信息查询](docs/catalog.md)
- [性价比排行：已核验 / 参考 / 综合](docs/rankings.md)
- [免费与试用入口](docs/trials.md)
- [三个参考仓库的逐项汇总范围](docs/coverage.md)
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

价格和容量对应**同一个入门套餐**；多周期套餐按同币种最低折合月费选取，显示真实支付金额。全年共用流量标为总量。来源记录可能过期，未知手续费未计入。

推荐指数采用[推荐依据](docs/recommendation.md)：★★★★★ 维护者长期主力推荐、★★★★☆ 来源当前主推、★★★☆☆ 来源普通收录、★★☆☆☆ 待核验候选；1/5 暂缓。维护者主力优先展示；来源等级不等于本仓库测速评分。

**优先推荐：[大哥云](providers/dageyun.md)** — 这是维护者主要使用的机场，稳定使用2年以上，未遇到问题；节点足够丰富，稳定性强，性价比高。（维护者个人体验，反馈于2026-10-13。）

### 有套餐资料

| 机场 | 参考价格 | 对应容量 | 推荐指数 | 线路 | 资料 |
| --- | --- | --- | --- | --- | --- |
| 大哥云 | 88 CNY/年（折合7.33/月） | 15 GB/月 | ★★★★★ · 维护者主力 | 待核验 | [查看](providers/dageyun.md) |
| 365VPN | 38.88 CNY/月 | 不限量（留意限速） | ★★★★☆ · 来源主推 | 官方客户端 | [查看](providers/365vpn.md) |
| Arisaka | 15.99 CNY/月 | 80 GB/月 | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/arisaka.md) |
| 贝贝云 | 249.9 CNY/年（折合20.82/月） | 100 GB/月 | ★★★★☆ · 来源主推 | 海外中转 | [查看](providers/beibei.md) |
| BoostNet | 200 CNY/年（折合16.67/月） | 20 GB/月 | ★★★★☆ · 来源主推 | 专线 / 透传 | [查看](providers/boostnet.md) |
| 次元雲 | 17 CNY/月 | 158 GB/月 | ★★★☆☆ · 来源收录 | 中转 | [查看](providers/ciyy.md) |
| E-IX | 199 CNY/年（折合16.58/月） | 1024 GB/年总量 | ★★★★☆ · 来源主推 | 透传专线 | [查看](providers/eix.md) |
| FlyBit | 15 CNY/月 | 128 GB/月 | ★★★☆☆ · 来源收录 | 中转 | [查看](providers/flybit.md) |
| 飞喵云 | 9.88 CNY/月 | 100 GB/月 | ★★★☆☆ · 来源收录 | 中转 | [查看](providers/fmyun.md) |
| 自由猫 | 12 CNY/月 | 100 GB/月 | ★★★☆☆ · 来源收录 | 中转 | [查看](providers/freecat.md) |
| 蜂窝云 | 20 CNY/月 | 200 GB/月 | ★★★☆☆ · 来源收录 | 中转 | [查看](providers/fwcloud.md) |
| 海獭 | 25 CNY/季（折合8.33/月） | 50 GB/月 | ★★★★☆ · 来源主推 | 中转 / 透传 | [查看](providers/haita.md) |
| happy猫 | 9.9 CNY/月 | 200 GB/月 | ★★★☆☆ · 来源收录 | 中转 | [查看](providers/happymao.md) |
| iNetS | 7.5 CNY/月 | 50 GB/月 | ★★★☆☆ · 来源收录 | 直连 优化 | [查看](providers/inets.md) |
| Just My Socks | 5.88 USD/月 | 500 GB/月 | ★★★★☆ · 来源主推 | 直连 | [查看](providers/jms.md) |
| Kycloud | 150 CNY/年（折合12.50/月） | 10 GB/月 | ★★★★☆ · 来源主推 | 专线 / 海外中转 | [查看](providers/kycloud.md) |
| 老猫云 | 45 CNY/季（折合15.00/月） | 50 GB/月 | ★★★★☆ · 来源主推 | 海外中转 | [查看](providers/laomao.md) |
| 良心云 | 2 CNY/月 | 100 GB/月 | ★★★☆☆ · 来源收录 | 直连 | [查看](providers/liangxin.md) |
| M78星云 | 12.8 CNY/月 | 150 GB/月 | ★★★☆☆ · 来源收录 | 中转 | [查看](providers/m78star.md) |
| 农夫山泉 | 15 CNY/月 | 200 GB/月 | 1/5 · 暂缓 | 中转 | [查看](providers/nfsq.md) |
| 念云 | 12 CNY/月 | 150 GB/月 | ★★★☆☆ · 来源收录 | 直连 优化 | [查看](providers/nianyun.md) |
| NyanSS | 7.5 CNY/月 | 50 GB/月 | 1/5 · 暂缓 | 中转 | [查看](providers/nyanss.md) |
| ofoNET | 12.87 CNY/月 | 200 GB/月 | ★★★☆☆ · 来源收录 | 中转 | [查看](providers/ofonet.md) |
| 壹速云 | 19.9 CNY/月 | 100 GB/月 | 1/5 · 暂缓 | 中转 | [查看](providers/onesy.md) |
| 赔钱机场 | 2.99 CNY/月 | 500 GB/月 | ★★★☆☆ · 来源收录 | 直连 | [查看](providers/peiqian.md) |
| 山海 | 15 CNY/月 | 128 GB/月 | ★★★★☆ · 来源主推 | 直连 / 中转 | [查看](providers/shanhai.md) |
| TAG | 154 CNY/年（折合12.83/月） | 200 GB/年总量 | ★★★★☆ · 来源主推 | 专线 | [查看](providers/tag.md) |
| 泰山机场 | 8.5 CNY/月 | 64 GB/月 | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/taishan.md) |
| 兔兔云 | 11.88 CNY/月 | 140 GB/月 | ★★★☆☆ · 来源收录 | 中转 | [查看](providers/tutuyun.md) |
| WgetCloud | 59 CNY/月 | 140 GB/月 | ★★★★☆ · 来源主推 | 专线 | [查看](providers/wgetcloud.md) |
| 一分机场 | 2 CNY/月 | 100 GB/月 | ★★★☆☆ · 来源收录 | 直连 | [查看](providers/yifen.md) |
| 一元机场 | 11 CNY/年（折合0.92/月） | 50 GB/月 | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/yiyuan.md) |
| 悠兔 | 199 CNY/年（折合16.58/月） | 200 GB/年总量 | ★★★★☆ · 来源主推 | 专线 / 中转 | [查看](providers/youtu.md) |

### 免费／试用及待核验候选

| 机场 | 参考价格 | 对应容量 | 推荐指数 | 线路 | 资料 |
| --- | --- | --- | --- | --- | --- |
| 爱翻机场 | 待核验 | 3天 / 10GB；来源称限速200Mbps（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/afun.md) |
| aimacloud | 待核验 | 6天 / 20GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/aimacloud.md) |
| alori | 待核验 | 6天 / 50GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/alori.md) |
| 翱翔云 | 待核验 | 7天 / 20GB；签到规则待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/aoxiang.md) |
| 白羊星 | 待核验 | 1天 / 5GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/baiyangxing.md) |
| 宝贝云 | 待核验 | 1天 / 2GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/baobei.md) |
| BBQ烧烤店 | 待核验 | 7天 / 10GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/bbq.md) |
| 白变小樱 | 待核验 | 3天 / 10GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/bbxy.md) |
| BCast | 待核验 | 6天 / 10GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/bcast.md) |
| besnow | 待核验 | 3天 / 9GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/besnow.md) |
| Bochidev | 待核验 | 不限时 / 50GB；领取规则待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/bochidev.md) |
| BT3rd-Speed | 待核验 | 6天 / 10GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/bt3.md) |
| 彩虹云 | 待核验 | 1天 / 10GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/caihong.md) |
| cd520 | 待核验 | 3天 / 5GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/cd520.md) |
| 中国国际机场 | 待核验 | 2天 / 15GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/china-international.md) |
| cocolink | 待核验 | 7天 / 64GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/cocolink.md) |
| 大牛机场 | 待核验 | 1小时 / 1GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/daniu.md) |
| 大迅云 | 待核验 | 2天 / 10GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/daxun.md) |
| 灯塔加速器 | 待核验 | 3天；额度待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/dengta.md) |
| 逗猫 | 待核验 | 1天 / 3GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/doucat.md) |
| edCloud | 待核验 | 待核验 | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/edcloud.md) |
| Free机场 | 待核验 | 公益节点；领取方式待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/free-airport.md) |
| freesocks | 待核验 | 免费节点；额度待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/freesocks.md) |
| FSCloud | 待核验 | 3天 / 10GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/fscloud.md) |
| 幽速101 | 待核验 | 公益节点；额度待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/ghost101.md) |
| GLaDOS | 待核验 | 4天 / 10GB；签到规则待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/glados.md) |
| 狗头加速器 | 待核验 | 5天 / 5GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/goutou.md) |
| ikuuu | 待核验 | 50GB；来源称不限时（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/ikuuu.md) |
| JetFast 极快代理 | 待核验 | 1个月 / 5GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/jetfast.md) |
| 加速啦 | 待核验 | 不限时 / 1GB；签到规则待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/jiasula.md) |
| 疾风 | 待核验 | 待核验 | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/jifeng.md) |
| 极光加速 | 待核验 | 2天 / 10GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/jiguang.md) |
| 极客加速器 | 待核验 | 3天 / 5GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/jike.md) |
| KELECLOUD | 待核验 | 1天 / 1GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/kelecloud.md) |
| 快乐星球 | 待核验 | 7天 / 10GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/kuailexingqiu.md) |
| 乐猫 | 待核验 | 30天 / 500GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/lemao.md) |
| 榴莲加速器 | 待核验 | 30天 / 100GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/liulian.md) |
| 猫熊网络加速器 | 待核验 | 3天 / 5GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/maoxiong.md) |
| Mickey | 待核验 | 3天 / 2GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/mickey.md) |
| 魔戒 | 待核验 | 试用价1元 / 2GB；期限待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/mojie.md) |
| 奈云 | 待核验 | 3天 / 5GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/naiyun.md) |
| 难民机场 | 待核验 | 2天 / 5GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/nanmin.md) |
| proxyvip | 待核验 | 1天 / 1GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/proxyvip.md) |
| qlgq | 待核验 | 7天 / 888GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/qlgq.md) |
| 闪电狗 | 待核验 | 3天 / 50GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/shandiangou.md) |
| 盛丰 | 待核验 | 5天 / 1GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/shengfeng.md) |
| sockboom | 待核验 | 1天 / 1GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/sockboom.md) |
| Speedy | 待核验 | 7天 / 10GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/speedy.md) |
| ssrsub | 待核验 | 来源称有零元活动；是否有效待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/ssrsub.md) |
| 速云 | 待核验 | 3天 / 10GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/suyun.md) |
| Synapse | 待核验 | 3天 / 5GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/synapse.md) |
| tly | 待核验 | 3天 / 2GB；签到规则待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/tly.md) |
| xqc.best | 待核验 | 来源称可能已无活动，待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/xqc.md) |
| 雨燕云 | 待核验 | 8小时 / 1GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/yuyan.md) |
| 纵横加速 | 待核验 | 7天 / 2GB（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/zongheng.md) |
| 纵云梯 | 待核验 | 不限时 / 1GB；签到规则待核验（活动记录） | ★★☆☆☆ · 待核验候选 | 待核验 | [查看](providers/zongyunti.md) |

### 已撤下的历史条目

| 机场 | 参考价格 | 对应容量 | 推荐指数 | 线路 | 资料 |
| --- | --- | --- | --- | --- | --- |
| 龙猫云 | 待核验 | 待核验 | 1/5 · 暂缓 | 待核验 | [查看](providers/longmaoyun.md) |
| 万达云 | 待核验 | 3GB；期限待核验（活动记录） | 1/5 · 暂缓 | 待核验 | [查看](providers/wandayun.md) |
| web3加速器 | 待核验 | 待核验 | 1/5 · 暂缓 | 待核验 | [查看](providers/web3.md) |
| 瑶瑶领先 | 待核验 | 待核验 | 1/5 · 暂缓 | 待核验 | [查看](providers/yylx.md) |


## 透明原则

价格按来源和核验日期公开；参考数据不冒充实测。推广链接不参与评分，默认全部使用无邀请码的入口，配置后可能包含推广收益。榜单按币种、重置方式分组，不通过猜测汇率混排。

仅检查公开网站，不公开用户订阅、节点凭据或账号信息。速度与解锁需要有日期、地区和运营商的测试证据。建议先短期验证自己的网络体验。

## 更新与贡献

每天北京时间 10:17 自动检查入口和参考来源，生成报告；每次提交自动校验数据和页面。资料修改用 JSON 单一来源，避免 README 与详情互相矛盾。参见 [维护说明](docs/maintenance.md) 和 [贡献流程](CONTRIBUTING.md)。

代码采用 MIT；社区参考仓库文章、截图与品牌标识未复制，相关权利归原作者。

# 贡献资料

提交新机场、套餐变化或实测记录时，提供公开来源URL、核验日期、币种、真实支付金额、流量周期、手续费和使用限制。使用问题模板；不提交用户订阅、支付订单、私人客服信息或节点凭据。

修改data与config后运行：

```bash
python3 scripts/catalog.py validate
python3 scripts/catalog.py generate
python3 -m unittest discover -s tests -v
```

不要直接改生成的README、providers、catalog/rankings/trials与导出文件；生成器会覆盖它们。购前指南等手写文档可直接编辑。质量评分需要可追溯实测依据，推广链接不改变排序。来源出现问题时先标watch，复核后恢复；保留历史证据。

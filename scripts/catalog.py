#!/usr/bin/env python3
"""Dependency-free catalog validation, deterministic publishing and terminal search."""
import argparse
import csv
import datetime as dt
import ipaddress
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit, quote

ROOT = Path(__file__).resolve().parents[1]
TODAY = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).date()

def read(path):
    return json.loads((ROOT / path).read_text())

def url_valid(value):
    u = urlsplit(value)
    if u.scheme != 'https' or not u.hostname or u.username or u.password or u.port not in (None,443):
        raise ValueError('URL must be a public HTTPS URL without credentials')
    if u.hostname == 'localhost' or '.' not in u.hostname:
        raise ValueError('local host prohibited')
    try:
        if not ipaddress.ip_address(u.hostname).is_global:
            raise ValueError('private IP prohibited')
    except ValueError as e:
        if str(e) == 'private IP prohibited':
            raise
    if re.search(r'(token|password|subscription|subscribe)=',value,re.I):
        raise ValueError('do not publish subscription credentials')
    return value

def load():
    return sorted((json.loads(p.read_text()) for p in (ROOT/'data').glob('*.json')),key=lambda p:p['id'])

def fresh(date,days):
    return bool(date and 0 <= (TODAY-dt.date.fromisoformat(date)).days <= days)

def unit_cost(plan):
    """Cost per 100 nominal usable GB; resets must never be conflated."""
    if plan['reset']=='unlimited' or not plan['traffic_gb']:
        return None
    total = plan['traffic_gb'] * (plan['billing_months'] if plan['reset']=='monthly' else 1)
    return plan['price'] * (1+(plan['fee_percent'] or 0)/100) / total * plan['multiplier'] * 100

def eligible(provider,plan):
    return provider['status'] not in ('watch','inactive') and fresh(plan['verified_at'],read('config/ranking.json')['stale_after_days'])

def validate(providers=None):
    providers = providers if providers is not None else load()
    ids=set(); sources={s['id'] for s in read('config/sources.json')}
    for source in read('config/sources.json'):
        url_valid(source['url']); dt.date.fromisoformat(source['reviewed_at'])
    for p in providers:
        assert re.fullmatch(r'[a-z0-9-]+',p['id']) and p['id'] not in ids, 'duplicate/invalid id'
        ids.add(p['id']); assert (ROOT/'data'/f"{p['id']}.json").exists()
        assert p['status'] in ('unverified','active','watch','inactive')
        assert p['name'] and p['sources'] and set(p['sources']) <= sources
        dt.date.fromisoformat(p['observed_at']); url_valid(p['official_url'])
        for url in p['mirrors']: url_valid(url)
        for x in p['plans']:
            assert x['source'] in sources and x['currency'] in ('CNY','USD','EUR','HKD')
            assert type(x['price']) in (int,float) and x['price']>0
            assert type(x['multiplier']) in (int,float) and x['multiplier']>0
            assert x['reset'] in ('monthly','total','unlimited')
            assert x['billing_months'] is None or type(x['billing_months']) is int and x['billing_months']>0
            assert x['reset']!='monthly' or x['billing_months'] is not None
            assert x['reset']=='unlimited' or type(x['traffic_gb']) in (int,float) and x['traffic_gb']>0
            assert x['fee_percent'] is None or 0<=x['fee_percent']<=100
            if x['verified_at']: assert dt.date.fromisoformat(x['verified_at'])<=TODAY
        if p['quality']:
            q=p['quality']; assert q['evidence'] and q['network'] and q['region']
            url_valid(q['evidence']); dt.date.fromisoformat(q['tested_at'])
            for key in read('config/ranking.json')['quality_weights']: assert 0<=q[key]<=100
    links=read('config/affiliate-links.json'); assert set(links)==ids,'affiliate ids must match data ids'
    for value in links.values():
        if value: url_valid(value)
    cfg=read('config/ranking.json'); assert abs(sum(cfg['quality_weights'].values())-1)<1e-9
    return providers

def md(s):
    return str(s).replace('|','\\|').replace('\n',' ').replace('<','&lt;').replace('>','&gt;')

def link(p):
    return read('config/affiliate-links.json').get(p['id']) or p['official_url']

def table(headers,rows):
    return '| '+' | '.join(headers)+' |\n| '+' | '.join('---' for _ in headers)+' |\n'+''.join('| '+' | '.join(md(v) for v in row)+' |\n' for row in rows)

def write(path,text):
    (ROOT/path).parent.mkdir(parents=True,exist_ok=True)
    (ROOT/path).write_text(text,encoding='utf-8')

def generate():
    ps=validate(); sources={s['id']:s for s in read('config/sources.json')}
    intro='# 机场资料库 · 套餐对比与性价比排行\n\n'
    intro+='[![检查](https://github.com/luluarthub/airport-guide/actions/workflows/ci.yml/badge.svg)](https://github.com/luluarthub/airport-guide/actions/workflows/ci.yml)\n\n'
    intro+=f'收录 **{len(ps)} 家服务、{sum(len(p["plans"]) for p in ps)} 个套餐**。覆盖专线、中转、直连、低价、全年流量包和不限时套餐。资料按来源整理，未亲测条目明确标记。\n\n'
    intro+='## 快速入口\n\n- [全部机场与信息查询](docs/catalog.md)\n- [性价比排行：已核验 / 参考 / 综合](docs/rankings.md)\n- [免费与试用入口](docs/trials.md)\n- [购前检查与场景选择](docs/buying.md)\n- [客户端与使用入门](docs/clients.md)\n- [故障排查与常见问题](docs/faq.md)\n- [入口检查与来源变更报告](reports/health.md)\n- [邀请码替换与自动维护](docs/maintenance.md)\n- [来源与数据说明](docs/sources.md)\n\n'
    intro+='## 按需求查找\n\nGitHub 页面内可使用浏览器搜索；每家都有独立资料页。需要多条件筛选可下载仓库后运行：\n\n```bash\npython3 scripts/catalog.py search --query 海獭\npython3 scripts/catalog.py search --route 直连 --max-monthly 20 --currency CNY\npython3 scripts/catalog.py search --protocol AnyTLS --reset total\n```\n\n'
    intro+='预算筛选按折合月费，全年共用与不限时包单独标识；真实支付金额见详情。下载 [JSON](reports/catalog.json) 或 [CSV](reports/plans.csv) 可在表格中筛选全部套餐。\n\n'
    intro+='## 机场概览\n\n'
    rows=[]; trial=[]; exported=[]
    for p in ps:
        entry=f"[详情](../providers/{p['id']}.md)"; official=f"[官方入口]({p['official_url']})"; register=f"[注册入口]({link(p)})"
        rows.append([p['name'],p['route'],' / '.join(p['protocols']),p['status'],entry,official])
        text=f"# {p['name']}\n\n{official} · {register}\n\n"
        text+=f"资料观察日期：{p['observed_at']}；运营状态：{p['status']}（unverified=未实测，watch=来源提示问题）。\n\n"
        text+=f"线路记录：{p['route']}\n\n协议记录：{' / '.join(p['protocols'])}\n\n客户端限制：{p['client_policy']}\n\n设备限制：{p['device_limit'] or '待核验'}\n\n地区：{'、'.join(p['regions']) or '待官网核验'}\n\n备注：{p['notes']}\n\n## 套餐\n\n"
        prows=[]
        for x in p['plans']:
            fee=f"{x['fee_percent']}%" if x['fee_percent'] is not None else '待核验'
            unit=unit_cost(x); period=f"{x['billing_months']}个月" if x['billing_months'] else '不限时'
            flow=f"{x['traffic_gb']:g} GB" if x['traffic_gb'] else '不限量（留意限速）'
            prows.append([x['name'],f"{x['price']:g} {x['currency']}",period,flow,x['reset'],fee,f'{unit:.2f}' if unit is not None else '不参与流量排名',x['verified_at'] or '社区参考 / 待核验'])
            exported.append({'provider':p['name'],'id':p['id'],**x,'cost_per_100gb':unit,'registration_url':link(p)})
        text+=table(['套餐','支付金额','付费周期','额度','重置周期','手续费','每100GB价格（原币）','官网核验日期'],prows)
        text+='\nmonthly=每月重置；total=整个有效期共用；unlimited=不限量。倍率暂按1计算，实际节点倍率另查。手续费未知时单价不含手续费。\n\n## 信息查询入口\n\n'
        details=p.get('details',{})
        if details:
            labels={'udp':'UDP','payment':'付款方式','ssh_port':'SSH端口限制','mail_protocols':'邮件协议限制','service_restrictions':'服务访问限制','support':'客服','overseas_access':'境外使用条件','unlock_claim':'解锁记录'}
            text+=table(['项目','来源记录（待实测）'],[[label,details.get(key) or '待核验'] for key,label in labels.items()])+'\n'
        name=quote(p['name']+' 机场')
        text+=f"- {official}：查套餐、公告、工单、客服和退款规则\n- [GitHub 公开信息检索](https://github.com/search?q={name}&type=repositories)\n- [公开资料检索](https://www.google.com/search?q={name})：搜索结果须自行确认同名与仿冒问题\n- [报告问题](https://github.com/luluarthub/airport-guide/issues/new/choose)\n"
        text+=''.join(f'- [社区评测入口 {i}]({url})：第三方历史记录，注意日期与测试环境\n' for i,url in enumerate(p.get('review_links',[]),1))
        text+='\n## 资料来源\n\n'+''.join(f"- [{sid}]({sources[sid]['url']})；资料核对日期 {sources[sid]['reviewed_at']}\n" for sid in p['sources'])
        text+='\n[返回全部机场](../docs/catalog.md) · [查看排名方法](../docs/rankings.md)\n'
        write(f"providers/{p['id']}.md",text)
        if p['trial']: trial.append([p['name'],p['trial'],entry,official,'社区记录 / 待核验'])
    catalog='# 全部机场与查询入口\n\n状态为资料标记，不是实时可用性。入口可达不代表代理节点可用。\n\n'+table(['机场','线路','协议','状态','资料','查询入口'],rows)
    write('docs/catalog.md',catalog)
    intro+=table(['机场','线路','资料'],[[p['name'],p['route'],f"[查看](providers/{p['id']}.md)"] for p in ps])
    intro+='\n## 透明原则\n\n价格按来源和核验日期公开；参考数据不冒充实测。推广链接不参与评分，默认全部使用无邀请码的入口，配置后可能包含推广收益。榜单按币种、重置方式分组，不通过猜测汇率混排。\n\n仅检查公开网站，不公开用户订阅、节点凭据或账号信息。速度与解锁需要有日期、地区和运营商的测试证据。建议先短期验证自己的网络体验。\n\n## 更新与贡献\n\n每天北京时间 10:17 自动检查入口和参考来源，生成报告；每次提交自动校验数据和页面。资料修改用 JSON 单一来源，避免 README 与详情互相矛盾。参见 [维护说明](docs/maintenance.md) 和 [贡献流程](CONTRIBUTING.md)。\n\n代码采用 MIT；社区参考仓库文章、截图与品牌标识未复制，相关权利归原作者。\n'
    write('README.md',intro)
    ranking='# 性价比排行\n\n价格单价只是一个维度。低价格不代表节点稳定、解锁可靠或未来持续运营。\n\n**每100GB成本 = 支付价格 × (1 + 已知手续费) ÷ 可用流量 × 节点倍率 × 100**。月重置流量乘付费月数；全年共用和不限时流量不乘。未知手续费与倍率差异另行核验。\n\n榜单展示每家在该组的最低单位成本套餐，保留真实预付金额。美元与人民币分组；不限量套餐没有可比流量单价。\n\n'
    for verified in (True,False):
        ranking+=('## 官网已核验套餐价格榜\n\n' if verified else '## 社区参考价格榜（待官网核验）\n\n')
        ranking+='已核验只代表公开套餐价格核验，运营质量仍待实测。\n\n' if verified else '这些价格来自社区，可能过期；本榜用于查资料，不构成实测推荐。watch与inactive条目被排除。\n\n'
        groups={}
        for p in ps:
            if p['status'] in ('watch','inactive'): continue
            for x in p['plans']:
                cost=unit_cost(x)
                if cost is None or eligible(p,x)!=verified: continue
                groups.setdefault((x['currency'],x['reset']),{}).setdefault(p['id'],[]).append((cost,p,x))
        if not groups: ranking+='暂无符合条件的套餐。\n\n'
        for (currency,reset),items in sorted(groups.items()):
            best=sorted((min(options,key=lambda v:v[0]) for options in items.values()),key=lambda v:(v[0],v[1]['id']))
            ranking+=f'### {currency} · {reset}\n\n'+table(['排名','机场','套餐','每100GB','实际支付','核验'],[[i,f"[{p['name']}](../providers/{p['id']}.md)",x['name'],f'{cost:.2f}',f"{x['price']:g} {currency}",x['verified_at'] or '待核验'] for i,(cost,p,x) in enumerate(best,1)])+'\n'
    cfg=read('config/ranking.json'); ranked=[]
    for p in ps:
        q=p['quality']
        if q and p['status']=='active' and fresh(q['tested_at'],cfg['stale_after_days']):
            score=sum(q[k]*v for k,v in cfg['quality_weights'].items())
            ranked.append((score,p,q))
    ranking+='## 实测综合体验评分\n\n权重：稳定性40%、速度25%、解锁15%、客服20%。各项0–100，必须提供公开测试证据、测试日期、地区与运营商；90天后过期。此评分单独呈现，不把价格单价和人工评分强行合并。\n\n'
    ranking+=table(['评分','机场','测试日','网络','证据'],[[f'{score:.1f}',p['name'],q['tested_at'],q['network'],f"[记录]({q['evidence']})"] for score,p,q in sorted(ranked,key=lambda x:-x[0])]) if ranked else '暂无本仓库实测数据，因此暂不发布综合推荐名次。\n'
    write('docs/rankings.md',ranking)
    write('docs/trials.md','# 免费与试用入口\n\n活动可能变化，以下为社区记录，注册前以官方当前规则为准。免费和试用均不等于永久免费。\n\n'+table(['服务','试用记录','详情','官方入口','核验'],trial)+'\n## 免费工具官方查询\n\n- [迷雾通 Geph](https://geph.io/)：免费层与使用条件请查官方\n- [Lantern](https://github.com/getlantern/lantern)：下载与免费额度请查官方\n\n不汇总来源未知的共享订阅。相关社区线索见 [来源](sources.md)。\n')
    write('reports/catalog.json',json.dumps(ps,ensure_ascii=False,indent=2)+'\n')
    with (ROOT/'reports/plans.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(exported[0])); writer.writeheader(); writer.writerows(exported)
    print(f'Generated {len(ps)} providers')

def search(args):
    for p in validate():
        if args.query and args.query.casefold() not in json.dumps(p,ensure_ascii=False).casefold(): continue
        if args.route and args.route not in p['route']: continue
        if args.protocol and args.protocol.casefold() not in ' '.join(p['protocols']).casefold(): continue
        plans=[x for x in p['plans'] if (not args.currency or x['currency']==args.currency) and (not args.reset or x['reset']==args.reset) and (args.max_monthly is None or x['billing_months'] and x['price']/x['billing_months']<=args.max_monthly)]
        if not plans: continue
        print(json.dumps({'name':p['name'],'status':p['status'],'official_url':p['official_url'],'registration_url':link(p),'plans':plans},ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser(); sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('validate'); sub.add_parser('generate'); s=sub.add_parser('search')
    for field in ('query','route','protocol','currency','reset'): s.add_argument('--'+field)
    s.add_argument('--max-monthly',type=float)
    args=parser.parse_args()
    if args.command=='generate': generate()
    elif args.command=='validate': validate(); print('Validated')
    else: search(args)

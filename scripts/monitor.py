#!/usr/bin/env python3
"""Check public entrypoints and source diffs; never infer node availability."""
import concurrent.futures
import datetime as dt
import hashlib
import ipaddress
import json
import socket
import urllib.error
import urllib.request
from urllib.parse import urlsplit
from catalog import ROOT, load, read, validate, write, fresh, url_valid

MAX_BYTES=1024*1024

def public_url(url):
    url_valid(url)
    host=urlsplit(url).hostname
    addresses=socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
        raise ValueError('non-public address')
    return url

class PublicRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        public_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def check(item):
    key,url,kind=item
    try:
        public_url(url)
        request=urllib.request.Request(url,headers={'User-Agent':'airport-guide-public-link-check/1.0'})
        opener=urllib.request.build_opener(PublicRedirect())
        with opener.open(request,timeout=12) as response:
            body=response.read(MAX_BYTES+1)
            result={'id':key,'url':url,'kind':kind,'status':'reachable','http_code':response.status}
            if kind=='source':
                result['sha256']=hashlib.sha256(body).hexdigest() if len(body)<=MAX_BYTES else None
                result['status']='too_large' if len(body)>MAX_BYTES else 'reachable'
            return result
    except urllib.error.HTTPError as e:
        return {'id':key,'url':url,'kind':kind,'status':'restricted' if e.code in (401,403,429) else 'http_error','http_code':e.code}
    except Exception as e:
        return {'id':key,'url':url,'kind':kind,'status':'unknown','error_type':type(e).__name__}

def run():
    ps=validate(); stamp=dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat(timespec='seconds')
    old=read('reports/health.json') if (ROOT/'reports/health.json').exists() else {'checks':[]}
    previous={r['id']:r for r in old['checks']}
    targets=[('provider:'+p['id'],url,'entry') for p in ps for url in [p['official_url']]]
    targets += [('mirror:'+p['id']+':'+str(i),url,'entry') for p in ps for i,url in enumerate(p['mirrors'])]
    for source in read('config/sources.json'):
        url=source['url']
        if url.startswith('https://github.com/'):
            url='https://raw.githubusercontent.com/'+url.removeprefix('https://github.com/')+'/HEAD/README.md'
        targets.append(('source:'+source['id'],url,'source'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(check,targets))
    changes=[]
    for r in results:
        prev=previous.get(r['id'])
        if prev and r['status']!=prev['status']: changes.append(r['id']+': '+prev['status']+' → '+r['status'])
        if r['kind']=='source' and r.get('sha256'):
            # Preserve the accepted digest until a maintainer reviews the source.
            baseline=(prev or {}).get('baseline_sha256') or (prev or {}).get('sha256') or r['sha256']
            r['baseline_sha256']=baseline
            if baseline!=r['sha256']: changes.append(r['id']+': 来源正文变化，需复核')
    days=read('config/ranking.json')['stale_after_days']
    pending=[p['id'] for p in ps if any(not fresh(x['verified_at'],days) for x in p['plans'])]
    attention=sorted(changes+[r['id']+': '+r['status'] for r in results if r['status']!='reachable'])
    fingerprint=hashlib.sha256(json.dumps([attention,pending],ensure_ascii=False).encode()).hexdigest()
    report={'checked_at':stamp,'checks':results,'attention':attention,'pending_price_review':pending,'fingerprint':fingerprint}
    write('reports/health.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    text='# 入口与来源巡检\n\n最近运行：'+stamp+'（北京时间）\n\n检查位置：本机或 GitHub Actions 执行环境；不代表中国内地各运营商访问结果，也不代表节点可用性。403/429归类为访问限制，DNS/超时归类为未知，不自动认定跑路。首次运行只建立来源内容基线。\n\n'
    text+='| 对象 | 检查类型 | 状态 | HTTP |\n| --- | --- | --- | --- |\n'
    text+=''.join(f"| {r['id']} | {r['kind']} | {r['status']} | {r.get('http_code','—')} |\n" for r in results)
    text+='\n## 需关注\n\n'+('\n'.join('- '+x for x in attention) or '本次无入口状态变化或已知来源正文变化。')
    text+='\n\n## 待价格核验\n\n'+', '.join(pending)+'\n\n机器人只记录公开可达性和变更线索；不修改价格、排名证据或邀请码。\n'
    write('reports/health.md',text)
    write('reports/maintenance-issue.md','# 自动维护待办\n\n'+text+'\n\n来源复核后，将 health.json 中对应 baseline_sha256 更新为本次 sha256。套餐核验后更新 verified_at。\n')
    write('reports/notify.json',json.dumps({'notify':bool(attention or pending) and fingerprint!=old.get('fingerprint'),'fingerprint':fingerprint})+'\n')
    print(f'Checked {len(results)} public URLs; {len(attention)} attention items')

if __name__=='__main__': run()

"""Maintain one issue in the owning repository only when findings change."""
import json
import subprocess
from catalog import read, ROOT
if read('reports/notify.json')['notify']:
    result=subprocess.run(['gh','issue','list','--state','open','--search','自动维护待办 in:title','--json','number,title'],check=True,capture_output=True,text=True)
    items=[x for x in json.loads(result.stdout) if x['title']=='自动维护待办']
    if items:
        subprocess.run(['gh','issue','edit',str(items[0]['number']),'--body-file',str(ROOT/'reports/maintenance-issue.md')],check=True)
    else:
        subprocess.run(['gh','issue','create','--title','自动维护待办','--body-file',str(ROOT/'reports/maintenance-issue.md')],check=True)

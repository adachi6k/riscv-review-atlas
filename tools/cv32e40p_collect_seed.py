from pathlib import Path
import json,subprocess,concurrent.futures
p=Path(__file__).resolve().parents[1]/'.local/cv32e40p'
p.mkdir(parents=True,exist_ok=True)
if not (p/'index-pages.json').exists():
 r=subprocess.run(['gh','api','--paginate','--slurp','repos/openhwfoundation/cv32e40p/issues?state=all&per_page=100'],capture_output=True,text=True,check=True)
 (p/'index-pages.json').write_text(r.stdout)
rows={x['number']:x for page in json.load(open(p/'index-pages.json')) for x in page}
seeds=[1064,975,889,888,880,730,723,466,920,195,824,860,841,881,897]
def fetch(n):
 d=p/'seed-evidence'/str(n);d.mkdir(parents=True,exist_ok=True)
 (d/'record.json').write_text(json.dumps(rows[n],indent=2)+'\n')
 for name,endpoint in [('comments',f'issues/{n}/comments'),('timeline',f'issues/{n}/timeline')]:
  r=subprocess.run(['gh','api','--paginate','--slurp',f'repos/openhwfoundation/cv32e40p/{endpoint}?per_page=100'],capture_output=True,text=True,check=True);(d/f'{name}.json').write_text(r.stdout)
 if 'pull_request' in rows[n]:
  for name,endpoint in [('pull','pulls/'+str(n)),('reviews',f'pulls/{n}/reviews'),('inline',f'pulls/{n}/comments')]:
   args=['gh','api']+(['--paginate','--slurp'] if name!='pull' else [])+[f'repos/openhwfoundation/cv32e40p/{endpoint}'];r=subprocess.run(args,capture_output=True,text=True,check=True);(d/f'{name}.json').write_text(r.stdout)
  r=subprocess.run(['gh','api',f'repos/openhwfoundation/cv32e40p/pulls/{n}','-H','Accept: application/vnd.github.diff'],capture_output=True,check=True);(d/'change.diff').write_bytes(r.stdout)
 return n
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as e: print('collected',list(e.map(fetch,seeds)))

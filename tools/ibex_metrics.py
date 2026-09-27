import sys,json,pathlib,collections,hashlib,re,statistics
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools'));import ibex_pilot as p
raw=R/'.local/ibex';out=R/'investigations/ibex'
import tiktoken
enc=tiktoken.get_encoding('cl100k_base')
idx=json.loads((raw/'index.json').read_text())
measure={}
for name,body in [('title_metadata',False),('title_and_body',True)]:
 items=[dict(number=x['number'],title=x['title'],kind='pr' if 'pull_request' in x else 'issue',**({'body':x.get('body')} if body else {})) for x in idx]
 s=json.dumps(items,ensure_ascii=False);measure[name]={'bytes':len(s.encode()),'cl100k_base_tokens':len(enc.encode(s))}
results=[];summary={}
for mode,folder in [('full','jev'),('compact','jev-compact')]:
 records=[json.loads(f.read_text()) for f in (raw/folder).glob('*.json')]
 assert len(records)==30 and all('response' in x for x in records)
 for r in records:
  d=p.payload(r['number'],mode);fingerprint=hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True).encode()).hexdigest();assert fingerprint==r['fingerprint']
  results.append({'number':r['number'],'mode':mode,'input_sha256':r['fingerprint'],'model':r['response']['model'],'answers':r['response']['answers'],'usage':r['response']['usage']})
 it=sum(r['response']['usage']['input_tokens'] for r in records);ot=sum(r['response']['usage']['output_tokens'] for r in records)
 summary[mode]={'calls':len(records),'input_tokens':it,'output_tokens':ot,'input_cost_usd_at_list_price':it*0.042/1e6,'category_counts':dict(collections.Counter(r['response']['answers']['category']['choice'] for r in records)),'input_tokens_min':min(r['response']['usage']['input_tokens'] for r in records),'input_tokens_max':max(r['response']['usage']['input_tokens'] for r in records)}
lookup={(r['number'],r['mode']):r for r in results}
summary['category_agreement']=sum(lookup[n,'full']['answers']['category']['choice']==lookup[n,'compact']['answers']['category']['choice'] for n in p.SELECTED)
summary['compact_input_reduction_fraction']=1-summary['compact']['input_tokens']/summary['full']['input_tokens']
summary['total_input_tokens']=sum(summary[m]['input_tokens'] for m in ['full','compact']);summary['total_output_tokens']=sum(summary[m]['output_tokens'] for m in ['full','compact']);summary['total_input_cost_usd_at_list_price']=summary['total_input_tokens']*0.042/1e6
summary['hypothetical_threshold_0_7']={m:[n for n in p.SELECTED if lookup[n,m]['answers']['review_value']['noul']<0.7] for m in ['full','compact']}
metrics={'snapshot_date':'2026-09-28','repository':'lowRISC/ibex','head':json.loads((raw/'head.json').read_text())['sha'],'index_records':len(idx),'issues':sum('pull_request' not in x for x in idx),'pull_requests':sum('pull_request' in x for x in idx),'commit_records':len((raw/'commit-index.tsv').read_text().splitlines()),'title_fix_keyword_prs':sum('pull_request' in x and bool(re.search(r'\b(fix(?:es|ed)?|bug|incorrect)\b',x['title'],re.I)) for x in idx),'index_payload_proxy':measure,'jev':summary,'pricing_source':'https://docs.typesafe.ai/models','pricing_checked':'2026-09-28','pricing_usd_per_million_input_tokens':0.042,'notes':['cl100k_base is a payload-size proxy, not the Codex or Jev tokenizer or billing.','Jev usage is from API responses. List-price arithmetic is not an invoice.','Index sizes exclude comments, diffs, prompts, outputs and reasoning.','No actual Codex session token total or monetary cost is available.','Sample is purposive; agreement does not measure accuracy or recall.']}
(out/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n');(out/'jev-results.json').write_text(json.dumps(sorted(results,key=lambda x:(x['number'],x['mode'])),indent=2)+'\n');(out/'jev-questions.json').write_text(json.dumps(p.QUESTIONS,indent=2)+'\n')
print(json.dumps(metrics,indent=2))

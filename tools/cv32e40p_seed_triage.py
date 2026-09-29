"""Bounded full-evidence seed triage; raw source material and API responses stay local."""
import concurrent.futures, hashlib, json, os, urllib.request
from pathlib import Path
from ibex_evidence_assessment import validate
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'.local/cv32e40p'
OUT=ROOT/'investigations/cv32e40p'
GROUPS=[[1064],[975],[888,889,897],[880,881],[730,841],[723,824,860],[466],[920],[195]]
def run():
    OUT.mkdir(parents=True,exist_ok=True)
    cache=BASE/'jev';cache.mkdir(exist_ok=True)
    payloads=BASE/'payloads';payloads.mkdir(exist_ok=True)
    q=json.loads((ROOT/'investigations/ibex/full-evidence/questions.json').read_text())
    jobs=[]
    for members in GROUPS:
        atoms=[]
        for n in members:
            for f in sorted((BASE/'seed-evidence'/str(n)).iterdir()):
                atoms.append({'source':f'{n}/{f.name}','text':f.read_text()})
        evidence=json.dumps(atoms,ensure_ascii=False)
        chunks=[evidence[i:i+24000] for i in range(0,len(evidence),24000)]
        assert ''.join(chunks)==evidence
        for i,chunk in enumerate(chunks):
            state={'repository':'openhwfoundation/cv32e40p','members':members,'partition':{'index':i+1,'count':len(chunks),'partial':len(chunks)>1},'scope':'Selected seed records, complete collected comments/timeline and one-hop linked PR records/reviews/inline comments/final diff. Links are not proof of fixes. No attachments or recursively linked material. JSON text is losslessly partitioned; fragments may start within fields.','evidence_fragment':chunk}
            payload={'model':'jev-1.13.0','state':state,'questions':q}
            data=json.dumps(payload,ensure_ascii=False).encode();key=hashlib.sha256(data).hexdigest()
            (payloads/f'{key}.json').write_bytes(data)
            jobs.append({'id':key,'members':members,'part':i+1,'parts':len(chunks)})
    assert len(jobs)<=128,'Bounded seed budget exceeded'
    def one(job):
        path=cache/(job['id']+'.json')
        if path.exists():response=json.loads(path.read_text())
        else:
            data=(payloads/(job['id']+'.json')).read_bytes()
            req=urllib.request.Request('https://api.typesafe.ai/v1/systemone',data=data,headers={'Authorization':'Bearer '+os.environ['TYPESAFE_API_KEY'],'Content-Type':'application/json'})
            with urllib.request.urlopen(req,timeout=55) as reply:response=json.load(reply)
            validate(response,q);path.write_text(json.dumps(response)+'\n')
        validate(response,q)
        return {**job,'answers':{k:v['choice'] for k,v in response['answers'].items()},'usage':response['usage']}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:results=list(executor.map(one,jobs))
    summary={'model':'jev-1.13.0','seed_records':10,'collected_records':15,'groups':len(GROUPS),'successful_parts':len(results),'input_tokens':sum(x['usage']['input_tokens'] for x in results),'output_tokens':sum(x['usage']['output_tokens'] for x in results)}
    (OUT/'part-results.json').write_text(json.dumps(results,indent=2)+'\n')
    (OUT/'usage.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))
if __name__=='__main__':run()

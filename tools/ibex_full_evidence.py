"""Collect public Ibex evidence once, group linked records, and evaluate with Jev.

Raw evidence remains in ignored .local/. No model score is a current-defect finding.
"""
import argparse
from collections import defaultdict, Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import threading
import time
import urllib.request

from ibex_pilot import ROOT, RAW, MODEL, NoRedirect, save, diff_file_count, same_repo_references

BASE = RAW / 'full-evidence'
OUT = ROOT / 'investigations/ibex/full-evidence'
REPO = 'lowRISC/ibex'
PAGE = 'pageInfo { hasNextPage endCursor }'
REF = 'number url repository { nameWithOwner }'
EVENT_NODES = ('nodes { __typename ... on CrossReferencedEvent { source { '
               '... on Issue { '+REF+' } ... on PullRequest { '+REF+' } } } '
               '... on ClosedEvent { closer { ... on Commit { oid url } '
               '... on PullRequest { '+REF+' } } } }')
TIMELINE = 'timelineItems(first:20,itemTypes:[CROSS_REFERENCED_EVENT,CLOSED_EVENT]) { '+PAGE+' '+EVENT_NODES+' }'
REVIEW = 'reviews(first:20) { '+PAGE+' nodes { id body url state commit { oid } } }'
CLOSING = 'closingIssuesReferences(first:20) { '+PAGE+' nodes { '+REF+' } }'
COMMON = 'id number title body url updatedAt comments { totalCount } '+TIMELINE
QUERY = ('query($ids:[ID!]!) { rateLimit { cost remaining resetAt } nodes(ids:$ids) { '
         '__typename ... on Issue { '+COMMON+' } ... on PullRequest { '+COMMON+' '
         'baseRefOid headRefOid merged mergedAt mergeCommit { oid } changedFiles '+REVIEW+' '+CLOSING+' } } }')


def stamp():
    return datetime.now(timezone.utc).isoformat()


def gh(endpoint, *, query=None, variables=None, accept=None):
    cmd = ['gh', 'api', endpoint]
    content = None
    if query:
        cmd += ['--input', '-']
        content = json.dumps({'query': query, 'variables': variables or {}})
    if accept:
        cmd += ['-H', 'Accept: '+accept]
    for attempt in range(3):
        result = subprocess.run(cmd, input=content, capture_output=True, text=True, timeout=180)
        if result.returncode == 0:
            data = result.stdout if accept else json.loads(result.stdout)
            if query and data.get('errors'):
                raise RuntimeError(json.dumps(data['errors']))
            return data
        if attempt < 2:
            time.sleep(2 ** attempt)
    raise RuntimeError('GitHub read failed: '+endpoint+'; '+result.stderr[:300])


def repository_pages(name, endpoint):
    folder = BASE / name
    folder.mkdir(parents=True, exist_ok=True)
    data = []
    page = 1
    while True:
        path = folder / f'{page}.json'
        if path.exists():
            records = json.loads(path.read_text())
        else:
            records = gh(endpoint+f'?per_page=100&page={page}')
            save(path, records)
        data.extend(records)
        if len(records) < 100:
            return data
        page += 1


def collect():
    BASE.mkdir(parents=True, exist_ok=True)
    index = json.loads((RAW / 'index.json').read_text())
    baseline=json.loads((ROOT/'investigations/ibex/reading-triage/results.json').read_text())
    wanted={r['number'] for r in baseline}
    index=[r for r in index if r['number'] in wanted]
    if {r['number'] for r in index}!=wanted:raise RuntimeError('Source index is missing baseline members')
    if not (BASE / 'acquisition.json').exists():
        save(BASE / 'acquisition.json', {'started_at': stamp(), 'repository': REPO, 'index_records': len(index)})
    for label, endpoint in [('conversation', 'issues/comments'), ('inline', 'pulls/comments')]:
        data = repository_pages(label, f'repos/{REPO}/{endpoint}')
        save(BASE / (label+'.json'), data)
        print('Collected',label,len(data),flush=True)
    batches = [index[i:i+40] for i in range(0,len(index),40)]
    for i,batch in enumerate(batches):
        path = BASE / 'metadata-pages' / f'{i}.json'
        if not path.exists():
            data = gh('graphql', query=QUERY, variables={'ids':[r['node_id'] for r in batch]})
            save(path,data)
        if i % 10 == 0:
            print('Metadata batches',i+1,'/',len(batches),flush=True)
    records=[]
    for i,batch in enumerate(batches):
        data=json.loads((BASE / 'metadata-pages' / f'{i}.json').read_text())
        nodes=data['data']['nodes']
        if len(nodes)!=len(batch) or any(n is None for n in nodes):
            raise RuntimeError('Unavailable GraphQL record; do not claim complete coverage')
        if [n['id'] for n in nodes]!=[r['node_id'] for r in batch]:
            raise RuntimeError('Cached metadata batch differs from the selected index order')
        records.extend(nodes)
    for record in records:
        for field in ['timelineItems','reviews','closingIssuesReferences']:
            if field not in record:
                continue
            connection=record[field]
            while connection['pageInfo']['hasNextPage']:
                cursor=connection['pageInfo']['endCursor']
                path=BASE/'extra-pages'/f"{record['number']}-{field}-{hashlib.sha256(cursor.encode()).hexdigest()[:16]}.json"
                if path.exists():
                    extra=json.loads(path.read_text())
                else:
                    if field=='timelineItems':
                        args='first:100,after:$cursor,itemTypes:[CROSS_REFERENCED_EVENT,CLOSED_EVENT]'
                        nodes=EVENT_NODES
                    else:
                        args='first:100,after:$cursor'
                        nodes='nodes { id body url state commit { oid } }' if field=='reviews' else 'nodes { '+REF+' }'
                    query='query($id:ID!,$cursor:String!){node(id:$id){... on '+record['__typename']+'{'+field+'('+args+'){'+PAGE+' '+nodes+'}}}}'
                    extra=gh('graphql',query=query,variables={'id':record['id'],'cursor':cursor})['data']['node'][field]
                    save(path,extra)
                connection['nodes'].extend(extra['nodes'])
                connection['pageInfo']=extra['pageInfo']
    save(BASE/'metadata.json',records)
    print('Expanded metadata',len(records),flush=True)
    prs=[r for r in records if r['__typename']=='PullRequest']
    errors=[]
    def get_diff(record):
        n=record['number'];path=BASE/'diffs'/f'{n}.diff';path.parent.mkdir(exist_ok=True)
        if path.exists():
            return n
        try:
            diff=gh(f'repos/{REPO}/pulls/{n}',accept='application/vnd.github.diff')
            tmp=path.with_suffix('.tmp');tmp.write_text(diff);tmp.replace(path)
        except Exception as error:
            save(BASE/'diff-errors'/f'{n}.json',{'number':n,'error':str(error),'time':stamp()})
            errors.append(n)
        return n
    with ThreadPoolExecutor(max_workers=8) as pool:
        for i,_ in enumerate(pool.map(get_diff,prs),1):
            if i%100==0:print('Diffs processed',i,'/',len(prs),flush=True)
    print('Diff acquisition complete; failures',errors,flush=True)
    acquisition=json.loads((BASE/'acquisition.json').read_text());acquisition['collection_finished_at']=stamp();save(BASE/'acquisition.json',acquisition)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['collect']);args=parser.parse_args()
    collect()

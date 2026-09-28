"""Recover API-limited PR diffs from pinned Git comparisons, checking changed paths."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
from ibex_full_evidence import BASE, RAW, REPO, gh, stamp
from ibex_pilot import save


def run(cmd):
    result=subprocess.run(cmd,capture_output=True,timeout=600)
    if result.returncode:raise RuntimeError(result.stderr.decode(errors='replace')[:500])
    return result.stdout


def write_diff(number,data,method,extra=None):
    try:text=data.decode('utf-8');encoding='utf-8'
    except UnicodeDecodeError:text=data.decode('latin-1');encoding='latin-1-byte-mapping'
    path=BASE/'diffs'/f'{number}.diff';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    raw=BASE/'diff-raw'/f'{number}.bin';raw.parent.mkdir(exist_ok=True);raw.write_bytes(data)
    save(BASE/'diff-provenance'/f'{number}.json',{'number':number,'method':method,'raw_sha256':hashlib.sha256(data).hexdigest(),
        'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'decoding':encoding,'retrieved_at':stamp(),**(extra or {})})


def main():
    records={r['number']:r for r in json.loads((BASE/'metadata.json').read_text())}
    failures=[int(p.stem) for p in (BASE/'diff-errors').glob('*.json') if not (BASE/'diffs'/(p.stem+'.diff')).exists()]
    git=RAW/'git'
    for n in sorted(failures):
        r=records[n]
        failure=json.loads((BASE/'diff-errors'/f'{n}.json').read_text())
        if 'codec' in failure.get('error','') and 'decode' in failure.get('error',''):
            data=run(['gh','api',f'repos/{REPO}/pulls/{n}','-H','Accept: application/vnd.github.diff'])
            write_diff(n,data,'GitHub REST diff with reversible decoding');print('Recovered',n,flush=True);continue
        files=[];page=1
        while True:
            values=gh(f'repos/{REPO}/pulls/{n}/files?per_page=100&page={page}');files+=values
            if len(values)<100:break
            page+=1
        if len(files)!=r['changedFiles']:raise RuntimeError(f'GitHub file list coverage mismatch for {n}')
        run(['git','-C',str(git),'fetch','--filter=blob:none','origin',f'refs/pull/{n}/head:refs/atlas/pulls/{n}/head'])
        actual=run(['git','-C',str(git),'rev-parse',f'refs/atlas/pulls/{n}/head']).decode().strip()
        if actual!=r['headRefOid']:raise RuntimeError(f'Head moved for {n}; needs a new snapshot')
        base=r['baseRefOid'];head=r['headRefOid']
        try:run(['git','-C',str(git),'cat-file','-e',base+'^{commit}'])
        except RuntimeError:run(['git','-C',str(git),'fetch','--filter=blob:none','origin',base])
        merge_base=run(['git','-C',str(git),'merge-base',base,head]).decode().strip()
        paths=run(['git','-C',str(git),'diff','--no-ext-diff','--no-textconv','--find-renames','--name-only','-z',merge_base,head]).decode().split('\0')
        expected={f['filename'] for f in files}
        if set(filter(None,paths))!=expected:raise RuntimeError(f'Git/GitHub changed-path disagreement for {n}')
        data=run(['git','-C',str(git),'-c','core.quotepath=false','diff','--no-ext-diff','--no-textconv','--find-renames',merge_base,head])
        write_diff(n,data,'Local Git merge-base diff; changed-path set verified against paginated GitHub files',
                   {'base_sha':base,'head_sha':head,'merge_base_sha':merge_base,'verified_file_count':len(files)})
        print('Recovered',n,len(files),'files',len(data),'bytes',flush=True)

if __name__=='__main__':main()

import json,csv
from pathlib import Path
r=Path(__file__).resolve().parents[1]; p=r/'investigations/ibex/full-evidence'; out=p/'reading-priority'
out.mkdir(parents=True, exist_ok=True)
m={x['number']:x for x in json.load(open(r/'.local/ibex/full-evidence/metadata.json'))}
g=json.load(open(p/'group-results.json')); bynum={n:x for x in g for n in x['members']}
pilot={157,272,277,294,332,398,401,465,475,712,742,792,813,854,903,919,928,1054,1107,1136,1141,1234,1309,1744,1813,1883,2446,2501,2442,2439}
choices=[
(2166,'P1','Unexpected memory responses','Check that response/error handling requires an outstanding transaction; distinguish secure hardening from the non-secure protocol assumption.'),
(1469,'P1','Branch prediction recovery','Check ownership of the recovery PC when consecutive predicted branches overlap with a skid-buffer stall.'),
(2374,'P1','Expanded instruction interruption','Check abort-state reset, atomic commit and debug boundaries; read #2461 alongside the fix to separate manual checks from regression coverage.'),
(169,'P1','Faulting-load side effects','Check that a load error suppresses register writeback, including error/data arriving together.'),
(172,'P1','Illegal jump side effects','Check that illegal JALR does not redirect the PC or corrupt the exception PC.'),
(836,'P1','Stalled jump control','Check whether a preceding memory stall stretches jump control and repeats fetch activity.'),
(2178,'P1','RV32E source-register legality','Check the store-data register independently of the ALU immediate selection; confirm the reported behavior against the pinned implementation.'),
(2514,'P1','Reset can disable the checker','Inspect the proposed reset/checker restart tests and require nonzero checked progress after reset; this PR is unmerged in the snapshot.'),
(858,'P1','Protocol-checker correctness','Inspect both checker fixes and derive a negative test for the checker itself; do not assume checker assertions are a trustworthy oracle.'),
(2142,'P1','Unmapped-address handling','Check that decode misses produce errors rather than aliasing a real device; applicability is the example system/interconnect.'),
(713,'P2','Split instruction fault address','Check that mtval identifies the faulting half of a split instruction, rather than always the instruction start.'),
(1421,'P2','Split data fault address','Check the fault address for the second aligned transfer of a misaligned load/store; compare with the instruction-fetch case without conflating them.'),
(1747,'P2','Cache invalidation re-entry','Check that another invalidation request during an active invalidation does not request a new scrambling key.'),
(1036,'P2','Reserved shift encodings','Check all required encoding bits, including bits 26 and 25, when deciding shift-immediate legality.'),
(575,'P2','Pending versus enabled interrupts','Check that reading interrupt-pending state does not depend on interrupt-enable bits.'),
(1948,'P2','Reference-model mismatch','Separate permitted split-access behavior from a real RTL defect; inspect pending-access bookkeeping on PMP failure.'),
(2169,'P2','Configuration-dependent branch stall','Investigate the reported load/branch sequence with writeback enabled and no branch-target ALU; external reproducer is not included in the corpus.'),
(1835,'P2','Write-response integrity','Check the intended integrity-alert policy for write responses even though their data payload is unused; scope the security assumptions.'),
(2490,'P2','Reset-time PMP legality','Compare configurable PMP reset values with CSR-write WARL handling; validate the report and its parameter/specification assumptions before adopting a property.'),
(1135,'P2','Security feature combinations','Separate parameter legality, fetch-error PC checks and dummy-instruction checks into distinct candidate properties.')]
parts=json.load(open(p/'part-results.json')); costs={}
for x in parts:costs[x['group']]=costs.get(x['group'],0)+x['input_proxy_tokens']
rows=[]
for rank,(n,t,topic,why) in enumerate(choices,1):
 x=bynum[n]; a=m[n]
 assert x['route']=='deep_read' and not (set(x['members'])&pilot)
 rows.append(dict(rank=rank,priority=t,group=x['group'],representative=n,title=a['title'],url=a['url'],topic=topic,reading_question=why,source_status=('merged PR' if a.get('merged') else 'unmerged PR') if a['__typename']=='PullRequest' else 'issue report',members=x['members'],jev_route=x['route'],jev_novelty_labels=x['novelty_labels'],existing_property_hints=x['closest_existing'],payload_proxy_tokens=costs[x['group']],head_sha=a.get('headRefOid'),updated_at=a['updatedAt']))
assert len(rows)==20 and len({x['group'] for x in rows})==20
json.dump(rows,open(out/'top-20.json','w'),indent=2);(out/'top-20.json').open('a').write('\n')
selected={x['group']:x for x in rows}; classified=[]
for x in g:
 if x['group'] in selected: tier=selected[x['group']]['priority'];reason='Selected editorial reading shortlist'
 elif set(x['members'])&pilot:tier='covered';reason='Contains a source in the previous 30-record pilot; group may still contain unreviewed material'
 elif x['route']=='low_priority':tier='P5';reason='Jev low-priority route; retain for exclusion audits'
 elif x['route']=='fetch_evidence':tier='P4';reason='Resolve evidence or partition-context gaps before routine deep reading'
 else:tier='P3';reason='Remaining Jev deep-read candidates; deferred, not rejected'
 classified.append(dict(group=x['group'],priority=tier,reason=reason,members=x['members'],jev_route=x['route'],novelty_labels=x['novelty_labels'],payload_proxy_tokens=costs[x['group']]))
json.dump(classified,open(out/'all-groups.json','w'),indent=2);(out/'all-groups.json').open('a').write('\n')
with open(out/'all-groups.csv','w') as f:
 w=csv.writer(f);w.writerow(['group','priority','members','jev_route','payload_proxy_tokens','reason'])
 for x in classified:w.writerow([x['group'],x['priority'],' '.join(map(str,x['members'])),x['jev_route'],x['payload_proxy_tokens'],x['reason']])
from collections import Counter
counts=dict(Counter(x['priority'] for x in classified));total=sum(x['payload_proxy_tokens'] for x in rows)
lines=['# Ibex: prioritized reading shortlist','', 'Snapshot: 2026-09-29. This is a research reading order, **not bug severity or bug probability**. No new defects were reproduced for this selection.','', '## Selection method','', 'Reuse the completed full-evidence Jev triage of 1,804 retrieval groups (2,481 records), including comments, reviews and available final text diffs. Review candidate titles across the deep-read groups with new/mixed-property labels, then inspect selected source descriptions to establish concrete reading questions. The final ordering is editorial, not an additional Jev score or an exhaustive human comparison of all 807 deep-read groups. No additional Jev calls were made.','', 'Priorities favor an explicit failure mechanism or falsifiable check, potential additions beyond the existing 24 properties, reusable lessons across configurations, and manageable reading scope. Topic diversity is deliberate. Small inputs alone do not determine rank. Previous pilot groups are excluded from the top 20. A retrieval group can contain several unrelated changes: shared references are not proof of one root cause.','', 'P1 contains ten cases to read first; P2 contains ten subsequent cases that are more specialized, require additional adjudication, or complement P1. P3 retains other deep-read candidates. P4 requires evidence/context follow-up. P5 is retained for exclusion audits. `covered` only means the group intersects the previous pilot, not that every member was read. P4/P5 are workflow dispositions, not claims that their defects are less important.','', 'Classification counts: '+', '.join(f'{k}: {v}' for k,v in sorted(counts.items()))+'.','', '## Top 20','', '| Rank | Priority | Entry | Topic | Snapshot status | Group payload proxy |','|---:|---|---|---|---|---:|']
for x in rows:lines.append(f"| {x['rank']} | {x['priority']} | [#{x['representative']}]({x['url']}) | {x['topic']} | {x['source_status']} | {x['payload_proxy_tokens']:,} |")
lines += ['', '## What to confirm','']
for x in rows:
 lines += [f"### {x['rank']}. {x['topic']} ({x['priority']})",'',f"Start with [{x['title']}]({x['url']}). {x['reading_question']}",'', 'Related group sources: '+', '.join(f"[#{n}]({m[n]['url']})" for n in x['members'])+'.', '', 'Existing-property hints from Jev: '+(', '.join(x['existing_property_hints']) or 'none')+'. These hints and novelty labels require human adjudication.','']
lines += ['## Reading budget and next step','',f'The 20 complete group payloads total **{total:,} cl100k proxy tokens** (P1: {sum(x["payload_proxy_tokens"] for x in rows if x["priority"]=="P1"):,}; P2: {sum(x["payload_proxy_tokens"] for x in rows if x["priority"]=="P2"):,}). This measures prepared inputs, including repeated context/questions, not unique source text, actual Codex billing, or a time estimate. Read in batches of five; do not inject the whole set into one prompt.','', 'For each entry, read the relevant discussion and diff, record assumptions, trigger, oracle and source revision, then decide whether it adds a new property, extends an existing property, or should be rejected. Start at the representative entry and only expand related records as necessary. Merge status is snapshot metadata, not independent correctness validation. Issue reports and unmerged PR claims remain unverified here. External reproducers and attachments were not collected; fetch them selectively when needed.','', 'This replaces the earlier budget-first `next-batch.json` as the recommended reading order; that file remains as a historical queue proposal. Low-priority audits remain a separate task, not part of these top 20.','', '[Machine-readable top 20](top-20.json) · [All group classifications](all-groups.csv) · [Full triage report](../README.md)','']
(out/'README.md').write_text('\n'.join(lines))
print(counts);print('proxy total',total)

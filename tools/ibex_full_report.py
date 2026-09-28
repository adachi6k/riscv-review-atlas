"""Publish original summaries of the full-evidence assessment, not raw source."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
from ibex_full_evidence import BASE, OUT
from ibex_pilot import ROOT, SELECTED, save


def main():
    recoveries=[json.loads(f.read_text()) for f in (BASE/'diff-provenance').glob('*.json')]
    save(OUT/'diff-recovery.json',recoveries)
    commit_provenance=[]
    from ibex_pilot import diff_file_count
    for c in json.loads((BASE/'standalone-commits.json').read_text()):
        folder=BASE/'commits'/c['cache_alias'];md=json.loads((folder/'metadata.json').read_text());count=diff_file_count((folder/'change.diff').read_text())
        if count!=len(md['files']) or len(md['files'])>=300:raise ValueError('Standalone commit file coverage needs inspection')
        commit_provenance.append({'sha':c['sha'],'url':c['url'],'references':c['references'],'diff_files':count,'metadata_file_count':len(md['files']),'parents':[x['sha'] for x in md['parents']]})
    save(OUT/'standalone-commits.json',commit_provenance)
    summary=json.loads((OUT/'summary.json').read_text())
    if summary['missing_parts']:raise SystemExit('Refusing final report with unevaluated parts')
    pre=json.loads((OUT/'preflight.json').read_text())
    atom_count=len(json.loads((OUT/'atoms.json').read_text()))
    refinement_file=OUT/'context-refinements.json'
    refinements=json.loads(refinement_file.read_text()) if refinement_file.exists() else []
    groups=json.loads((OUT/'group-results.json').read_text())
    records=json.loads((OUT/'records.json').read_text());by_record={r['number']:r for r in records}
    metadata={r['number']:r for r in json.loads((BASE/'metadata.json').read_text())}
    parts=json.loads((OUT/'part-results.json').read_text())
    proxy=Counter();usage=Counter()
    for p in parts:proxy[p['group']]+=p['input_proxy_tokens'];usage[p['group']]+=p['usage']['input_tokens']
    # Small bounded queue. This is a planning proxy, not Codex billing telemetry.
    prior=set(SELECTED);available=[g for g in groups if not prior.intersection(g['members'])]
    audits=sorted([g for g in available if g['route']=='low_priority'],
                  key=lambda g:hashlib.sha256(('ibex-full-audit:'+g['group']).encode()).hexdigest())[:5]
    chosen=[{**g,'queue_purpose':'exclusion_audit'} for g in audits]
    budget=sum(proxy[g['group']] for g in audits)
    categories=['rtl','verification','verification_interface','integration','unclear']
    buckets={c:[] for c in categories}
    for g in available:
        if g['route']!='deep_read':continue
        category=next((c for c in categories if c in g['categories']),None)
        if category:buckets[category].append(g)
    for bucket in buckets.values():
        bucket.sort(key=lambda g:(not any(x in g['novelty_labels'] for x in ['new_candidate','mixed']),proxy[g['group']],len(g['members']),g['group']))
    while len(chosen)<30 and any(buckets.values()):
        for category in categories:
            if len(chosen)>=30:break
            while buckets[category]:
                g=buckets[category].pop(0)
                if budget+proxy[g['group']]<=100_000:
                    chosen.append({**g,'queue_purpose':'deep_read'});budget+=proxy[g['group']];break
    queue=[]
    for g in chosen:
        prs=[n for n in g['members'] if by_record[n]['kind']=='PullRequest']
        representative=min(prs or g['members'])
        queue.append({'group':g['group'],'representative':representative,'title':metadata[representative]['title'],'url':by_record[representative]['url'],
                      'all_members':g['members'],'queue_purpose':g['queue_purpose'],'categories':g['categories'],
                      'novelty_labels':g['novelty_labels'],'closest_existing':g['closest_existing'],
                      'planning_proxy_tokens':proxy[g['group']]})
    save(OUT/'next-batch.json',{'status':'Proposed only; no additional source-level review performed',
        'selection':'Exclude groups containing the previous 30 pilot PRs. Five deterministic low-priority audits, then category-diverse deep-read groups preferring new/mixed leads and smaller payloads. At most 30 groups and 100,000 sum of prepared-payload cl100k_base proxy tokens.',
        'planning_proxy_tokens':budget,'warning':'A group can contain several source records. This proxy includes Jev questions and is not a Codex input or billing limit. Reassess before expanding detailed reading beyond the representatives.',
        'records':queue})
    with (OUT/'queue.csv').open('w',newline='') as f:
        fields=['group','route','baseline_group_route','members','parts_expected','categories','novelty_labels','closest_existing','evidence_gaps']
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for g in groups:w.writerow({k:';'.join(map(str,g[k])) if isinstance(g[k],list) else g[k] for k in fields})
    previous=json.loads((ROOT/'investigations/ibex/reading-triage/summary.json').read_text())
    bygroup={g['group']:g for g in groups}
    pilot_routes=Counter(bygroup[by_record[n]['group']]['route'] for n in SELECTED)
    top=sorted(usage,key=usage.get,reverse=True)[:10]
    costs=[{'group':g,'members':bygroup[g]['members'],'parts':bygroup[g]['parts_expected'],'input_tokens':usage[g],
            'share_of_input':usage[g]/summary['input_tokens']} for g in top]
    save(OUT/'cost-concentration.json',costs)
    collection={'source_records':len(records),'pull_requests':sum(r['kind']=='PullRequest' for r in records),
                'conversation_comments':sum(r['conversation_comments'] for r in records),
                'inline_review_comments':sum(r['inline_comments'] for r in records),
                'review_summaries':sum(r['review_summaries'] for r in records),
                'standalone_commits':pre['standalone_commits'],'diff_recoveries':len(json.loads((OUT/'diff-recovery.json').read_text())),
                'records_with_collection_gaps':sum(bool(r['gaps']) for r in records)}
    save(OUT/'collection-summary.json',collection)
    acquisition=json.loads((BASE/'acquisition.json').read_text())
    acquisition['final_report_generated_at']=datetime.now(timezone.utc).isoformat();save(OUT/'acquisition.json',acquisition)
    lines=['# Ibex: evaluate the evidence before deciding what to read','',
        '**Result:** every record in the 2,481-record source index was included in a completed Jev assessment with collected conversations, reviews and available linked code diffs. The unit is now a connected retrieval group, not an individual title/body record. This is triage, not an independently verified bug list.','',
        '## What changed','',
        'The preceding title/body pass left many records needing more context. This pass collects the evidence first, then asks Jev whether detailed human/Codex reading is worthwhile, which subject is involved, whether a property may go beyond the existing 24-item checklist, and what evidence is still missing.','',
        '```mermaid','flowchart LR','    A[Issue and PR index] --> B[Comments, reviews, links and diffs]','    B --> C[Group related records]','    C --> D[Preserve and partition large evidence]','    D --> E[Jev: reading action and checklist relation]','    E --> F[Bounded source review and exclusion audits]','```','',
        '## Collection and completeness','',
        '| Material | Collected |','| --- | ---: |',
        f"| Source issue/PR records | {collection['source_records']:,} |",
        f"| PR text diffs | {collection['pull_requests']:,} |",
        f"| Conversation comments | {collection['conversation_comments']:,} |",
        f"| Inline review comments | {collection['inline_review_comments']:,} |",
        f"| Review summaries/states, including empty bodies | {collection['review_summaries']:,} |",
        f"| Explicitly linked standalone commit diffs | {collection['standalone_commits']} |",
        f"| Connected retrieval groups | {summary['retrieval_groups']:,} |",
        f"| Evaluated inputs | {summary['evaluated_parts']:,} |",'',
        f"The collected text totals **{pre['unique_evidence_bytes']:,} UTF-8 bytes** before repeated prompt/partition context. **{pre['multipart_groups']} groups** required multiple inputs; the largest group contains {pre['largest_group_members']} records. All {summary['planned_parts']:,} planned inputs have successful responses. Collection-count/file-coverage gaps recorded at packaging time: **{pre['groups_with_collection_gaps']} groups**.",'',
        'Conversation counts were reconciled with record metadata. GraphQL pagination was followed for review summaries, cross-reference/closure events and declared closing references. Inline comments include their supplied historical diff hunks. Each PR diff has a file-header count matching changed-file metadata. Explicit standalone-commit diffs also match the collected file lists.','',
        'Ten PR diffs needed recovery: nine exceeded GitHub diff API limits and were generated from pinned local Git merge-base/head comparisons, with changed paths checked against paginated GitHub file lists; one contained non-UTF-8 bytes and was decoded with a reversible Latin-1 byte mapping. Original recovery bytes and hashes are cached locally. See [recovery provenance](diff-recovery.json).','',
        f'All **{atom_count:,} text atoms** were reconstructed from their ordered partition fragments and checked against source-text SHA-256 hashes and character lengths. This proves lossless partitioning of the captured, normalized text; it is not a claim that every HTTP byte stream or historical revision was archived verbatim.','',
        '**Scope limits:** the original 2026-09-28 index fixes membership, while comments and metadata were fetched later; GitHub is not a transactionally frozen snapshot. Final available PR diffs are included, not every intermediate patch revision. Attachments, binary contents, external repositories and full surrounding source trees were not ingested. Timeline collection covers cross-reference and closure events; other event kinds, including commit-reference events without an explicit collected link, are not exhaustively traversed. Bare abbreviated commit hashes without explicit repository URLs are not exhaustively resolved. General PR-to-PR or issue-to-issue references are indexed but not recursively expanded into the same input. Missing context can therefore remain even with complete collection for this declared scope.','',
        '## Grouping and partition decisions','',
        'Issue-to-PR references, closure information and matching commit revisions connect retrieval groups. Several records pointing to one explicitly linked standalone commit are grouped. General references are not asserted to be fixes. Each record and PR diff is stored in one group and partitioned once; inline historical review snippets can intentionally repeat code. This is retrieval deduplication, not proof that a group describes one root cause.','',
        'Small groups are sent together. Large groups are split into exact contiguous fragments with hashes and character offsets, retaining record identifiers/titles and a partial-context flag. A planning guard uses at most roughly 72 KB and 18,000 cl100k_base tokens for packed fragments; prompts and record context add overhead. This tokenizer is a proxy, not Jev billing. Eight calibration inputs, including the largest proxy inputs, were accepted before the full run.','',
        f"Jev rejected {len(refinements)} initial or refined inputs with its native token-limit error. Those inputs alone were subdivided, preserving every fragment and all successful cached requests. [Refinement provenance](context-refinements.json) links parent inputs to final children. Initial partition indexes remain in each payload; the group manifest lists the current leaf inputs.", '',
        'Group routing is deliberately conservative: any part requesting a deep read selects the group; otherwise a missing part, collection gap, a fetch-evidence answer, or multiple parts retains it for context review. Only a complete single-input low-priority group is deferred. Multipart scores are not maximized or interpreted as bug probabilities. More parts create more opportunities for a positive reading signal, so group size is not evidence of severity.','',
        '## Before/after reading actions','',
        'For comparison, the earlier per-record title/body actions were regrouped over exactly these same members: any deep-read member makes a deep-read baseline group; otherwise any fetch-evidence member makes a fetch-evidence group. This aligns the units, but questions, grouping and collection time also changed. **It is not a controlled accuracy or input-only effect measurement.**','',
        '| Action | Regrouped title/body baseline | Comments and diffs included |','| --- | ---: | ---: |']
    for route in ['deep_read','fetch_evidence','low_priority']:
        lines.append(f"| `{route}` | {summary['baseline_group_routes'].get(route,0):,} | {summary['group_routes'].get(route,0):,} |")
    lines += ['', '| Baseline → evidence route | Groups |','| --- | ---: |']
    for row in summary['group_transition_matrix']:lines.append(f"| `{row['from']}` → `{row['to']}` | {row['groups']} |")
    lines += ['',f"The 30 previously reviewed pilot PRs inherit these group actions: {dict(pilot_routes)}. This is a sanity check, not an independent evaluation set. Inspect individual part answers before treating a group action as a conclusion about a member.",'',
        f"**{summary['groups_with_new_candidate']} groups** contain at least one `new_candidate` or `mixed` checklist-relation answer. These are model-generated leads beyond the existing 24 properties, not that many confirmed new properties or bugs. The existing checklist has not been expanded automatically.",'',
        '## Measured usage and feasibility','',
        '| Pass | API input tokens | API output tokens | Input list-price calculation |','| --- | ---: | ---: | ---: |',
        f"| Earlier title/body routing | {previous['input_tokens']:,} | {previous['output_tokens']:,} | ${previous['input_list_price_usd']:.6f} |",
        f"| This assessment with comments and diffs | {summary['input_tokens']:,} | {summary['output_tokens']:,} | ${summary['list_price_usd_successful_input']:.6f} |",'',
        f"This pass uses **{summary['input_tokens']/previous['input_tokens']:.1f}×** the earlier API input. Prices use $0.042 per million input tokens and free output for pinned `jev-1.13.0`, checked against [official model documentation](https://docs.typesafe.ai/models) on 2026-09-29. Counts are API-reported successful-response usage; cost is arithmetic, not an invoice. Recorded failed attempts: {summary['failed_attempts']}; failures without usage are excluded. The eight calibration successes are included once through request-hash caching.",'',
        'The whole-evidence pass is feasible at this observed Jev cost, but it is not free of collection time or large-input overhead. Actual Codex session token totals/savings are unavailable. Jev reading millions of tokens does not mean those tokens were sent to Codex for source review. Final mechanism confirmation, applicability, oracle design and reproduction still require targeted work.','',
        '| Largest input-cost group | Source members | Inputs | API input tokens | Share |','| --- | --- | ---: | ---: | ---: |']
    for row in costs[:5]:
        members=', '.join(f'#{n}' for n in row['members'][:8])+(' …' if len(row['members'])>8 else '')
        lines.append(f"| {row['group']} | {members} | {row['parts']} | {row['input_tokens']:,} | {row['share_of_input']:.1%} |")
    lines += ['', 'Full members and exact costs are in [cost concentration](cost-concentration.json). Large vendoring/generated-content changes can dominate token consumption. They were retained in this experiment; a later explicitly scoped policy could treat such content separately, but this run did not silently omit it.','',
        '## Next bounded review queue','',
        f"The proposed queue contains **{len(queue)} groups**: {sum(r['queue_purpose']=='deep_read' for r in queue)} deep-read leads and {sum(r['queue_purpose']=='exclusion_audit' for r in queue)} low-priority audits. The sum of prepared-payload proxy tokens is **{budget:,}**, below the 100,000 planning ceiling. This includes Jev questions and is only a conservative planning metric, not actual Codex billing. Representatives are starting points; expanding to every member requires reassessing the detailed-reading budget.",'',
        'Selection excludes groups containing the previous pilot PRs, rotates across correctness categories, prefers new/mixed checklist leads and smaller payloads, and reserves deterministic low-priority audits. The queue has not been independently source-reviewed.','',
        '| Representative | Upstream title (lead, not verified finding) | Purpose | Existing property matches |','| --- | --- | --- | --- |']
    for r in queue:
        words=r['title'].split();title=' '.join(words[:20])+(' …' if len(words)>20 else '')
        title=title.replace('|','/').replace('<','&lt;').replace('>','&gt;').replace('[',r'\[').replace(']',r'\]')
        lines.append(f"| [#{r['representative']}]({r['url']}) | {title} | {r['queue_purpose']} | {', '.join(r['closest_existing']) or 'none'} |")
    lines += ['', '## Artifacts and reproduction','',
        '- [Group results](group-results.json), [part results](part-results.json), [sortable queue](queue.csv), and [next-batch selection](next-batch.json).',
        '- [Records](records.json), [groups](groups.json), [text-atom hashes](atoms.json), [relations](relations.json), and [standalone commits](standalone-commits.json).',
        '- [Exact questions](questions.json), [preflight](preflight.json), [usage summary](summary.json), and [acquisition timestamps](acquisition.json).','',
        'Use Python 3, authenticated GitHub CLI, Git, and `tiktoken` for proxy sizing. Raw evidence stays under ignored local storage and credentials are supplied through the environment; only original summaries, links, hashes and typed evaluation outputs are published. Upstream material retains its original licenses.','',
        '```sh','python3 tools/ibex_pilot.py index','python3 tools/ibex_full_evidence.py collect',
        '# For API-limited diffs, a blob-filtered clone must exist at .local/ibex/git.',
        'python3 tools/ibex_diff_fallback.py','python3 tools/ibex_evidence_assessment.py supplement',
        'python3 tools/ibex_evidence_assessment.py prepare',
        '# Provide TYPESAFE_API_KEY via your environment or secret manager.',
        'python3 tools/ibex_evidence_assessment.py evaluate --calibrate --workers 8',
        'python3 tools/ibex_evidence_assessment.py evaluate --workers 16',
        'python3 tools/ibex_evidence_assessment.py summarize','python3 tools/ibex_full_report.py',
        "python3 -m unittest discover -s tools -p 'test_*.py' -v",'```','',
        'Requests use payload-hash caches and per-request process locks. Native token-limit rejections cause lossless input refinement. Up to two retries are allowed only for transient HTTP 429/502/503/504 responses and are recorded. Other failures stop new submissions. A 200-million-input-token guardrail stops further requests in a run, with already in-flight requests allowed to finish; it is not a strict invoice limit. No RTL simulation, formal verification or new bug reproduction was performed by this pass.']
    (OUT/'README.md').write_text('\n'.join(lines)+'\n')
    print('Report written; queue groups:',len(queue),'planning proxy:',budget)


if __name__=='__main__':main()

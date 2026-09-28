# Ibex historical-review pilot

**Result:** 30 historical PRs collected, 28 used to derive **24 candidate review properties**, and two broad changes deferred. Jev evaluated the same 30 cases with both compact and detailed inputs. This is a bounded pilot for [investigation #2](https://github.com/adachi6k/riscv-review-atlas/issues/2), not an exhaustive investigation or a new-bug report.

- [Candidate checklist](checklist.md) / [JSON](checklist.json)
- [Case provenance and dispositions](cases.json)
- [Measured usage](metrics.json), [per-case Jev results](jev-results.json), [exact questions](jev-questions.json)

## Source and coverage

Snapshot: **2026-09-28**, canonical repository [lowRISC/ibex](https://github.com/lowRISC/ibex), public HEAD `7cd891ef267e8db36813b29cb8851142ab2636d5`. The source LICENSE at that revision was inspected: Apache-2.0. These original summaries do not relicense upstream code or discussions.

The GitHub all-issues endpoint yielded **2,481 records: 921 issues and 1,560 PRs**. A blob-filtered clone yielded **3,089 commit records reachable from fetched refs**; this is an index, not a review of every commit or deleted history. Counts are a dated snapshot, not a transactionally frozen GitHub dataset.

The pilot deliberately selected debug, trap, PMP, memory, counter and verification changes. It is **purposive, not random or representative**. Of the 30 selected PRs, **28 were merged and two (#2439 and #2442) were unmerged proposals**. The latter support candidate questions only; they are not evidence of accepted fixes. The selection is fixed in the collector. A title-only whole-word search for `fix`, `fixes`, `fixed`, `bug` or `incorrect` finds 344 PRs, but keyword matches neither define all defects nor establish relevance.

For each selected PR, collection included metadata, commit SHAs, changed paths, the complete available text diff, conversation comments, inline review comments, and one-hop same-repository issue/PR references from the body and conversation. Diff file-header counts matched reported changed-file counts. This checks file coverage, not semantic completeness. Raw evidence is cached locally and excluded from publication.

**Excluded:** a complete timeline/review-summary-event traversal, external references, image contents, recursive linked-history traversal, exhaustive comment collection for the other records, semantic inspection of every hunk, and independent test execution. PR base/head SHAs and actual merge SHAs are preserved; the API merge SHA for an unmerged proposal is labeled separately because it may describe a test merge; affected revision ranges were not established. GitHub metadata and comments can change after the snapshot.

## What the history contributed

The [checklist](checklist.md) records applicability, proposed stimulus and an independent oracle. It includes:

- coherent debug entry, cause, PC and privilege state;
- protection-error lifetime, PMP overlap priority and minimum-granularity boundaries;
- fault ownership across empty or younger pipeline stages;
- valid retirement counting and explicit counter-write arbitration;
- verification configuration, trace ownership, test-generator operands and unexpected-trap handling.

Related PRs are grouped by property. One PR can also support two distinct properties: #2446 concerns both retirement qualification and software-write arbitration. Consequently, 30 PRs does not mean 30 independent bugs or checklist entries. #332 and #398 remain deferred because their broader changes require a separate mechanism review.

Two examples show why titles and initial explanations are insufficient:

- [#903](https://github.com/lowRISC/ibex/pull/903): the discussion changes the proposed handling of PMP address matching. Extraction must follow the final mode-specific comparison, not just the initial proposal.
- [#1883](https://github.com/lowRISC/ibex/pull/1883): the RTL change affects verification-visible exception attribution. Its description explicitly distinguishes this from an architectural functional bug. It belongs in the verification-interface category even though the changed file is RTL.

No RTL simulation, formal proof or co-simulation was executed. Assertions were observed in #919 and #928, but were not run. The entries are **source-reviewed candidates** (22 linked to merged fixes and two to unmerged proposals), not independently reproduced findings or claims of defects at snapshot HEAD. Cross-core applicability remains untested.

## Jev experiment and token use

The model was pinned to `jev-1.13.0`. Each call answered three fixed questions: change category, reusable-review value, and evidence insufficiency. Upstream text was framed as untrusted evidence. Scores are not calibrated bug probabilities.

Two inputs were evaluated for each of the same 30 PRs:

| Input | Contents | Calls | API input tokens | API output tokens | Input list-price calculation |
| --- | --- | ---: | ---: | ---: | ---: |
| Detailed | Metadata, comments, linked records and full selected diff | 30 | 117,685 | 2,730 | $0.004943 |
| Compact | Title, body and changed paths | 30 | 21,689 | 2,730 | $0.000911 |
| Actual experiment total | Both passes | 60 | 139,374 | 5,460 | $0.005854 |

Prices use the official model documentation checked on 2026-09-28: **$0.042 per million input tokens; output free**. These are arithmetic estimates, not an invoice. See [Jev model documentation](https://docs.typesafe.ai/models) and [API documentation](https://docs.typesafe.ai/api). Usage counts are from API responses, not a local tokenizer.

Compact inputs used **81.6% fewer Jev input tokens** than detailed inputs. Categories agreed in **30/30 cases**: 26 RTL and four verification. Agreement between two model passes is not correctness. In particular, both categorized #1883 as RTL; the evidence review assigns it to the verification interface. The pilot taxonomy is too coarse for this distinction.

A hypothetical review-value cutoff of 0.70 would retain all detailed cases, but drop five compact cases: #398, #919, #928, #1234 and #1309. Four of those five contributed checklist properties after evidence review. This is an illustration of lost context, **not a validated threshold or a measured population false-negative rate**. No case was discarded by that score in this pilot.

### Can the investigation finish within a realistic token budget?

**A bounded checklist investigation is practical; an exhaustive deep review of every repository is not justified by this pilot.** The bottleneck is evidence interpretation and eventual validation, not these measured Jev API charges.

A reproducible `cl100k_base` measurement of the 2,481-record index gives:

| Serialized payload | Proxy input tokens |
| --- | ---: |
| Number, kind and title | 68,364 |
| Number, kind, title and body | 635,999 |

These figures exclude comments, diffs, instructions, outputs, reasoning and repeated context. They are **payload proxies**, not Codex billing or Jev token counts. The current Codex session's actual total and monetary cost are unavailable; no measured Codex savings are claimed. Even the index is too large to treat as a single economical review prompt. Deep evidence would add substantially more input.

Jev can offload structured triage. It does not replace tracing the fix, forming an independent oracle or running a reproduction. The detailed pass consumed extra tokens in this experiment; a production workflow should only promote selected or uncertain cases to that pass. Because this sample was already selected for likely relevance, it cannot estimate the yield or recall of repository-wide triage.

## Follow-up: ask Jev what deserves detailed reading

A subsequent [whole-index routing pass](reading-triage/README.md) asks Jev to choose between detailed reading, evidence fetching and low priority. It publishes every route, measured API usage and a proposed 25-case reading queue plus five exclusion audits. The inputs are title/body only; this does not complete source-level review or establish recall.

## Follow-up: collect comments and diffs before triage

The [assessment with comments and diffs](full-evidence/README.md) completes a further Jev pass with all PR text diffs, collected conversations/reviews and explicit linked standalone commits. It compares regrouped baseline actions and measured API usage; model leads remain unverified.

## Proposed continuation with explicit limits

1. **Index locally.** Reuse the cached issue/PR and commit indexes. Deduplicate linked issues and fixing PRs before extracting properties; retain separate evidence records.
2. **Compact Jev triage.** Process records individually or in bounded batches; add `verification-interface` and `mixed` categories. Separate reusable value from evidence sufficiency. Retain uncertain and sparsely described records for an evidence-fetch queue. Never reject only on a low value score.
3. **Bound detailed review.** Continue in batches of at most 30 new PRs. Use a planning ceiling of 100,000 `cl100k_base` evidence-input tokens per batch; split a batch when it exceeds that ceiling. This is a future payload limit, not a cap on model reasoning, context replay or billed tokens. Oversized changes get a named follow-up rather than silent truncation.
4. **Audit exclusions.** Include at least five low-score, no-fix-keyword or otherwise excluded leads per batch; record the selection rule. This can expose misses but is not enough to establish recall. Trace relevant non-PR commits separately instead of treating the PR index as complete history.
5. **Stop and compare.** After two further batches (at most 90 PRs including this pilot), report new versus duplicate properties, unresolved mechanisms, payload use and actual Jev usage. If two consecutive batches add no new properties within a declared topic scope, mark that scope provisionally saturated, not the repository exhaustively reviewed. Otherwise leave explicit backlog items and reassess the budget before expanding.
6. **Validate a small subset.** Choose 3–5 properties with clear applicability and an independent oracle before investing in historical or cross-core reproduction. Keep simulation/tooling cost separate from extraction cost.

This turns an open-ended history-reading exercise into a deliverable with visible coverage and leftovers. Investigation #2 remains open for wider coverage and validation.

## Reproduction of the collection and measurements

Requirements: Python 3, authenticated GitHub CLI, network access; `tiktoken` only for proxy measurement. Run from this repository. Collection is read-only on GitHub. Jev evaluation sends public evidence to its API and consumes API usage.

```sh
python3 tools/ibex_pilot.py index
python3 tools/ibex_pilot.py collect
# Supply TYPESAFE_API_KEY through your environment/secret manager.
python3 tools/ibex_pilot.py evaluate --mode full
python3 tools/ibex_pilot.py evaluate --mode compact
python3 -m unittest discover -s tools -p 'test_*.py' -v
```

For the commit index, use a blob-filtered clone under `.local/ibex/git` and save `git log --all --format='%H%x09%s'` to `.local/ibex/commit-index.tsv`. With the original cached snapshot and `tiktoken` installed, run `python3 tools/ibex_metrics.py` to regenerate metrics, questions and result summaries. Fresh collection can differ because upstream metadata is mutable; it is not a byte-identical archival reproduction.

Responses are cached by complete serialized-request SHA-256. Inputs over 96,000 bytes are skipped and recorded; this conservative pilot byte limit is not a general token-limit guarantee. Errors stop evaluation without automatic retries. The 60 calls above completed without skipped inputs. Raw caches and credentials are not published. Three offline boundary tests cover nested patch headers, same-repository link extraction and invalid API values; these are collector checks, not hardware tests.

# Checklist entry format

Each future entry should contain:

| Field | Purpose |
| --- | --- |
| ID and title | Stable identifier and concise review question |
| Property | What must remain true, independent of upstream signal names |
| Applicability | ISA, privilege, pipeline, cache/MMU, bus, and configuration prerequisites |
| Source evidence | Repository, issue/PR/MR URLs, affected and fixing revisions |
| Mechanism | Evidence-supported explanation; mark unresolved hypotheses |
| Review locations | State, ownership, handshake, cancellation, or update paths to inspect |
| Stimulus | How to exercise the relevant condition |
| Observation and oracle | Reachability evidence and an independent expected result |
| Verification record | Tool/configuration/commands/results, or explicitly not run |
| Evidence state | Reported, source-reviewed, fix-linked, regression-linked, or independently-reproduced |
| Lineage and duplicates | Shared patches, inherited fixes, related questions |
| Limitations | Missing evidence, exclusions, and inapplicable configurations |

The [Ibex pilot](../investigations/ibex/checklist.md) publishes source-reviewed candidate entries, distinguishing merged fixes from unmerged proposals. The CV32E40P pilot adds one `independently-reproduced-component` entry: this explicitly means a bounded component reproduction, not full-core validation. The repository catalog and investigation tickets are inputs to this process, not completed verification.

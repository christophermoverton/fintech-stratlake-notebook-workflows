# Notebook 14 Runtime Smoke Audit Summary

## Scope and Evidence Posture

This record covers optional Issue #147 runtime smoke evidence for
`notebooks/14_stratlake_campaign_evidence_review_pack_and_governance_audit.ipynb`.
All smoke sessions were run outside committed source by executing a temporary
notebook copy per session. The committed Notebook 14 source remains output-free,
unexecuted, preview-default, and gated.

This record is runtime observation only. It is not CI evidence, not
source/runtime-equivalence proof, and not a production, promotion, deployment,
governance-approval, or live-trading-readiness determination. Source-safe
import evidence remains separate in
[Notebook 14 import audit](notebook_14_import_audit.md).

## Runtime Environment Summary

Three separate smoke sessions were executed across distinct profiles. Each
session used a temporary notebook copy; no executed artifact was committed to
the repository.

Session A (`evidence_governance_preview`) used a local notebook execution
environment through the project Python environment and Jupyter nbconvert. No
external-storage mount was required. All runtime action gates were disabled.

Session B (`campaign_feature_restore_and_generation_run`) was executed in a
Colab runtime with Drive access. The session demonstrated Drive mount, isolated
archive restore, native `features_daily` feature-root discovery and adoption,
and native campaign preflight and execution.

Session C (`existing_campaign_evidence_governance_review`) was executed with an
existing operator-reviewed strategy run identity
(`momentum_v1_single_06d57faf4de5`). The session demonstrated native derived
evidence-review pack build and review and governance artifact observation. No
restore, feature-root adoption, or new campaign generation was performed.

## Profile and Gate Record

### Session A — Preview Only

Selected temporary runtime profile:

- `evidence_governance_preview`

Intentionally enabled gates:

- None.

Gates confirmed disabled in the temporary execution:

- `RUN_STRATLAKE_INIT`
- `RUN_ARCHIVE_RESTORE`
- `RUN_NATIVE_CAMPAIGN_GENERATION`
- `RUN_EVIDENCE_REVIEW_PACK_BUILD`
- `RUN_EVIDENCE_REVIEW_PACK_VALIDATE`
- `RUN_PROMOTION_GOVERNANCE_REPORT`
- `RUN_CATALOG_LINEAGE_EXPORT`
- `RUN_ARCHIVE_CHECKPOINT`
- `RUN_NOTEBOOK_RUNTIME_SUMMARY_WRITE`

### Session B — First-Run Restore and Campaign Generation

Selected temporary runtime profile:

- `campaign_feature_restore_and_generation_run`

Intentionally enabled gates:

- `RUN_STRATLAKE_INIT`
- `RUN_ARCHIVE_RESTORE`
- `RUN_NATIVE_CAMPAIGN_GENERATION`

### Session C — Existing-Campaign Evidence and Governance Review

Selected temporary runtime profile:

- `existing_campaign_evidence_governance_review`

Intentionally enabled gates:

- `RUN_STRATLAKE_INIT`
- `RUN_EVIDENCE_REVIEW_PACK_BUILD`
- `RUN_EVIDENCE_REVIEW_PACK_VALIDATE`
- `RUN_PROMOTION_GOVERNANCE_REPORT`

## Observed Actions and Outcomes

### Session A — Preview Only

| Action category | Outcome | Bounded result classification | Artifact inference or selection | Caveats |
|---|---|---|---|---|
| Temporary notebook load and execution | Succeeded | Preview-only runtime observation | No repository artifact was selected or inferred. | Executed artifact stayed outside committed source. |
| Profile selection | Succeeded | `evidence_governance_preview` observed | No campaign, run, review, archive, or policy identity was selected. | Does not prove native command availability or source/runtime equivalence. |
| Workspace initialization | Skipped | Gate disabled | No workspace initialization artifact was inferred. | Not a native workspace readiness check. |
| Drive or external-storage mount | Skipped | Gate disabled and not required | No external-storage artifact was selected. | Local runtime reported only preview diagnostics. |
| Archive restore | Skipped | Gate disabled | No archive or restored artifact was selected. | Phase B prerequisites were not supplied. |
| Campaign generation | Skipped | Gate disabled | No campaign artifact was created or selected. | No campaign readiness is claimed. |
| Evidence-review build | Skipped | Gate disabled | No derived review pack was created or selected. | Native evidence-review command was not used. |
| Strict evidence-review validation | Skipped | Gate disabled | No validation output was created or selected. | No validation result is claimed for this session. |
| Governance report | Skipped | Gate disabled | No governance artifact was created or selected. | No governance approval or decision is claimed. |
| Catalog/lineage observation | Skipped | Gate disabled | No catalog or lineage artifact was created or selected. | Not a catalog completeness check. |
| Checkpoint or runtime-summary write | Skipped | Gate disabled | No checkpoint or runtime summary was committed. | Temporary executed notebook output remains outside Git. |

### Session B — First-Run Restore and Campaign Generation

| Action category | Outcome | Bounded result classification | Artifact inference or selection | Caveats |
|---|---|---|---|---|
| Workspace initialization | Succeeded | Notebook initialization and environment checks observed | No repository artifact was selected or inferred. | Does not prove source/runtime equivalence. |
| Drive or external-storage mount | Succeeded | Drive mount observed | No repository storage artifact was selected. | Executed artifact stayed outside committed source. |
| Archive restore | Succeeded | Isolated archive restore observed | Restored archive identity was operator-selected. | No production archive state is claimed. |
| Feature-root discovery and adoption | Succeeded | Restored native `features_daily` inputs discovered and adopted | Feature root was explicitly reviewed before adoption. | Does not establish canonical feature completeness. |
| Campaign generation | Succeeded | Native campaign preflight and execution observed | Campaign artifact identity was run-local. | No campaign quality, alpha validity, or promotion readiness is claimed. |
| Evidence-review build | Skipped | Gate disabled | No derived review pack was created in this session. | Session was bounded to restore and campaign generation only. |

### Session C — Existing-Campaign Evidence and Governance Review

| Action category | Outcome | Bounded result classification | Artifact inference or selection | Caveats |
|---|---|---|---|---|
| Workspace initialization | Succeeded | Environment checks observed | No repository artifact was selected or inferred. | Does not prove source/runtime equivalence. |
| Archive restore | Skipped | Not applicable | No archive restore; existing campaign identity used. | Profile explicitly prohibits restore. |
| Feature-root adoption | Skipped | Not applicable | No feature-root adoption; existing campaign identity used. | Profile explicitly prohibits feature-root adoption. |
| Campaign generation | Skipped | Not applicable | No new campaign generation. | Profile explicitly prohibits campaign generation. |
| Evidence-review build | Succeeded | Native derived evidence-review pack build observed | Strategy run `momentum_v1_single_06d57faf4de5` was explicitly selected. | Derived pack is non-authoritative and rebuildable. |
| Strict evidence-review validation | Succeeded | `status: warn` observed | Native `validation.json` was observed as bounded runtime evidence. | No repair, bypass, or reinterpretation was performed. |
| Governance report | Succeeded | Read-only governance artifact observation | No unsupported promotion claims were made. | Governance observation is display-only and non-authoritative. |

## Native Validation and Governance Observations

Native strict validation was attempted in Session C
(`existing_campaign_evidence_governance_review`). The native `validation.json`
reported `status: warn`, not `fail`.

```text
required_files_written: pass
path_portability: pass
manifest_inventory_parity: pass
report_generated: pass
html_generated: na
diagnostics_overall_status: warn
overall status: warn
```

Native strict validation reported a warning; Notebook 14 did not repair,
bypass, or reinterpret the native result.

There are no failed checks, missing-file counts, invalid-file counts, or
invalid-file lists in the native validation result. The remaining warning
should be traced through canonical strategy, review, metrics, manifest, and
registry evidence. No notebook-owned repair, fallback, or validation
replacement is appropriate.

Native governance reporting was observed in Session C. The observation was
read-only and display-oriented. No governance approval or decision is claimed.

## Non-Claims and Handoff Boundaries

This smoke does not establish:

- review-pack completeness;
- canonical evidence completeness;
- engine correctness;
- policy compliance;
- promotion eligibility;
- promotion approval;
- governance approval;
- production readiness;
- deployment readiness;
- live-trading suitability;
- source/runtime equivalence.

Verified engine dependencies or native command defects belong in
`christophermoverton/stratlake-trade-engine`. This smoke does not assert an
engine, package, schema, artifact, validator, or version-compatibility root
cause.

## Decision

`notebook_14_runtime_smoke_multi_session_observed`

This label means only that temporary executions of the three smoke profiles
completed with each session bounded to its selected profile and gates. It is
not a readiness, approval, validation, promotion, deployment, production, or
live-trading label.

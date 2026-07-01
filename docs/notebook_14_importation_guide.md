# Notebook 14 Importation Guide

## Purpose And Posture

Notebook 14
(`notebooks/14_stratlake_campaign_evidence_review_pack_and_governance_audit.ipynb`)
is a source-safe, gated, read-only companion for campaign evidence review packs
and governance observation. It helps operators preview command surfaces,
optionally run explicitly gated native workflows in temporary runtime copies,
observe native evidence-review and governance outputs, and prepare conservative
handoff notes.

Notebook 14 is not a production workflow, promotion-decision system,
replacement for engine validation, replacement for engine governance
reporting, campaign approval mechanism, strategy approval mechanism,
statistical-significance or alpha-validation surface, deployment-readiness
assessment, production-readiness assessment, or live-trading-readiness
assessment.

Committed Notebook 14 source remains output-free, execution-count-null,
preview-default, and non-claiming. It must not commit real environment paths,
Drive paths, run IDs, review IDs, archive IDs, credentials, logs, generated
artifacts, validation results, governance reports, checkpoints, or runtime
summaries.

## Importation Order And Prerequisites

Recommended Notebook 14 import order:

| Issue | Importation step |
|---|---|
| #141 | Staging and cleanup baseline |
| #142 | Runtime profile and command-surface classification |
| #143 | Source-safe static contracts |
| #144 | Derived-pack, validation, and governance-observation guardrails |
| #145 | Importation documentation and caveat summary |
| #146 | Final import audit and PR-readiness review |
| #147 | Optional runtime smoke verification |

Importing Notebook 14 must preserve these source-safe defaults:

- `evidence_governance_preview` remains the committed default.
- Code-cell outputs remain absent.
- Code-cell execution counts remain `null`.
- No real environment paths, Drive paths, run IDs, review IDs, archive IDs,
  secrets, logs, or generated artifacts are committed.
- All runtime actions remain explicitly gated.

## Primary Runtime Profile Summary

The full profile matrix lives in
[Notebook 14 command surface classification](notebook_14_command_surface_classification.md).
The primary profile model is:

| Profile | Source-safe status | Intended use | Key prerequisites | Permitted activity | Prohibited activity | Default posture |
|---|---|---|---|---|---|---|
| `evidence_governance_preview` | Source-safe. | Committed preview posture for source inspection and disabled runtime controls. | Valid notebook source only. | Preview intent and in-memory diagnostics if executed without mutation. | Workspace initialization, Drive mount, archive restore, feature discovery/adoption, campaign generation, review-pack build/validation, governance reporting, catalog/lineage export, checkpointing, runtime summary writes. | Sole committed default. |
| `campaign_feature_restore_and_generation_run` | Temporary runtime-only. | First-run restore and campaign-generation path when campaign inputs or artifacts are not already local. | Reviewed archive/root values and explicit gates for initialization, optional Drive mount, restore, feature-root adoption, input review, and native campaign execution. | Native workspace/session initialization, gated archive restore, restored feature discovery, explicitly gated feature-root adoption, native campaign preflight/execution, conservative artifact inspection. | Governance decisions, promotion-state repair, unreviewed feature adoption, notebook fabrication of feature data, readiness or approval claims. | Not default. |
| `existing_campaign_evidence_governance_review` | Temporary runtime-only. | Review-only continuation from an operator-confirmed existing campaign run. | Confirmed run identity, configured artifact root, optional reviewed review identity, and explicit review/governance gates. | Native evidence-review pack build when absent, contained pack-root resolution, native strict validation, native read-only governance reporting, optional catalog/lineage observation. | Archive restoration, Drive archive restore, campaign creation, execution-candidate config work, feature discovery/adoption, guessed run/review identity, campaign-preparation caveats. | Not default. |

Legacy profiles remain classified compatibility or historical/reference
surfaces and are not recommended primary workflows.

## Runtime Gating And Source-Safe Execution Posture

Runtime behavior requires both a compatible selected runtime profile and
explicit runtime permission gates. Major gate families include:

- `RUN_STRATLAKE_INIT`
- `RUN_ARCHIVE_RESTORE`
- `RUN_NATIVE_CAMPAIGN_GENERATION`
- `RUN_EVIDENCE_REVIEW_PACK_BUILD`
- `RUN_EVIDENCE_REVIEW_PACK_VALIDATE`
- `RUN_PROMOTION_GOVERNANCE_REPORT`
- `RUN_CATALOG_LINEAGE_EXPORT`
- `RUN_ARCHIVE_CHECKPOINT`
- `RUN_NOTEBOOK_RUNTIME_SUMMARY_WRITE`

Committed source does not enable these actions. This guide deliberately avoids
real environment-variable values, credentials, local paths, Drive mount points,
run identifiers, archive identifiers, or copy-paste-ready commands for a real
campaign.

## Review-Pack Discovery, Containment, And Preservation

Derived evidence-review packs are classified as
`derived_evidence_review_pack_non_authoritative`. They are not canonical
promotion-state evidence and must not be copied, moved, repaired, normalized,
rewritten, or treated as authoritative governance evidence.

Notebook 14 keeps review-pack discovery within the configured campaign artifact
root. The default root convention is:

```text
EVIDENCE_REVIEW_REPO_ROOT = CAMPAIGN_ARTIFACT_ROOT.parent
```

Repository-relative native output roots are resolved from
`EVIDENCE_REVIEW_REPO_ROOT` and accepted only if contained by
`CAMPAIGN_ARTIFACT_ROOT`. No fallback root outside the configured artifact tree
is permitted. `_notebook_14_runtime` material is excluded from reviewable
evidence discovery.

Existing-pack discovery is lazy and bounded by
`NOTEBOOK14_EXISTING_EVIDENCE_PACK_DISCOVERY_LIMIT`. One additional directory
entry may be observed only to determine whether scanning was truncated.
Truncation means discovery may be incomplete. Automatic existing-pack selection
is allowed only when exactly one valid matching candidate is found after a
non-truncated scan. Ambiguity or truncation requires explicit
`NOTEBOOK14_REVIEW_ID` or a reviewed increase to the inspection limit.

Existing packs are preserved by default. Overwrite permission and existing-pack
validation permission remain separately gated. Notebook 14 does not claim
review-pack completeness, canonical status, policy compliance, or promotion
eligibility.

## M45 Promotion-State Ownership Summary

Promotion-state ownership remains separated:

- Review promotion state is review-owned.
- Campaign promotion state is campaign-owned.
- Canonical promotion-state construction, serialization, validation, and
  emission are engine-owned.
- Notebook 14 governance is observational, read-only, display-oriented,
  non-authoritative, and non-repairing.

Notebook 14 must not create, backfill, repair, normalize, rewrite,
reinterpret, or replay canonical promotion evidence. It must not merge campaign
and review state or borrow one as the other. It must not treat `not_reviewed`
as eligibility, approval, promotion, readiness, deployment readiness,
production readiness, or live-trading suitability.

For the canonical no-policy condition, preserve this exact sentence:

```text
No promotion policy was configured; no promotion decision was made.
```

## Native Strict-Validation Caveat And Engine Handoff

Native strict validation remains authoritative when explicitly invoked in a
permitted temporary runtime. Notebook 14 may display bounded diagnostics only,
including command text, executed/skipped state, return code, bounded
stdout/stderr tails, selected identities, effective roots, and display-only
observation of engine-written `validation.json`.

Notebook 14 must not replace native validation, copy engine schemas, repair or
normalize review-pack JSON, bypass native failure, weaken failure status, or
assert a root cause.

A native evidence-review pack build may succeed while native strict validation
reports invalid schema-governed review-pack JSON files. Treat that condition
only as an engine-owned package, contract-resource, validator, or
version-compatibility follow-up until independently verified. The Notebook 14
repository must not claim that it has proven an engine defect, package defect,
schema defect, artifact defect, or any specific root cause.

Use this conservative statement:

```text
Native strict validation reported a failure; Notebook 14 did not repair, bypass, or reinterpret the native result.
```

Expected handoff path:

- Retain the native failure result and bounded diagnostics as observation.
- Do not create a notebook workaround.
- Route a verified dependency issue to `christophermoverton/stratlake-trade-engine`.
- Keep notebook-side notes limited to observed symptoms, command outcome,
  selected identities, effective roots, and caveats.
- Do not assert that notebook and engine runtimes are equivalent.

## Import-Review Checklist

- Notebook 14 is valid JSON.
- Committed outputs are absent.
- All execution counts are `null`.
- `evidence_governance_preview` is the committed default.
- Runtime gates are disabled in committed source.
- No real runtime values or secrets are committed.
- Review-only exclusions remain preserved.
- Derived-pack discovery remains bounded, contained, and non-mutating.
- Truncated discovery cannot auto-select a pack.
- Native strict validation remains authoritative.
- Promotion-state ownership remains separated.
- No readiness, approval, production, deployment, or live-trading claims appear.


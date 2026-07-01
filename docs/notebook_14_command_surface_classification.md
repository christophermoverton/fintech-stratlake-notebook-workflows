# Notebook 14 Command And Runtime Surface Classification

## Purpose

Notebook 14
(`notebooks/14_stratlake_campaign_evidence_review_pack_and_governance_audit.ipynb`)
is a source-safe campaign evidence review and promotion-governance observation
notebook. It follows Notebook 13 by preserving preview, optional first-run
restore/campaign generation, and existing-campaign evidence/governance review
surfaces without becoming a replacement implementation for StratLake engine
logic.

This document classifies Notebook 14 runtime profiles, override templates,
native command authority, artifact classes, and M45 promotion-state boundaries.
It is source-only. It does not install packages, initialize a workspace, mount
Drive, restore archives, discover or adopt feature roots, run campaigns, build
or validate review packs, run governance, export catalog/lineage artifacts,
create checkpoints, or write notebook runtime summaries.

This classification does not claim campaign quality, alpha validity,
statistical significance, approval, promotion, governance readiness,
deployment readiness, production readiness, live-trading readiness, artifact
completeness, schema validity, or engine/runtime equivalence.

## Source And Runtime Posture

| Property | Value |
|---|---|
| Issue | #142 - M45.N14.2 - Classify Notebook 14 Runtime Profiles, Native Review, and Governance Observation Surfaces |
| Depends on | #141 - M45.N14.1 - Stage and Clean Notebook 14 Campaign Evidence Review and Governance Audit Workflow |
| Staging baseline | `10c4aad60bb0477079ad1abd44cd9b89937e660a` |
| Target notebook | `notebooks/14_stratlake_campaign_evidence_review_pack_and_governance_audit.ipynb` |
| Source posture | Cleaned, output-free, execution-count-null |
| Committed default profile | `evidence_governance_preview` |
| Primary first-run profile | `campaign_feature_restore_and_generation_run` |
| Primary review-only profile | `existing_campaign_evidence_governance_review` |
| Runtime artifact namespace | `_notebook_14_runtime/` |
| Runtime artifact posture | Noncanonical and excluded from reviewable evidence discovery |

## Classification Legend

| Category | Meaning |
|---|---|
| `primary` | Recommended operational profile for new Notebook 14 use. |
| `retained compatibility mode` | Kept for historical notebooks or operator continuity, but superseded by a primary profile for new use. |
| `historical/reference example` | Source-retained example or profile that documents lineage; not recommended for new runs. |
| `deprecated alias` | Legacy name that overlaps a primary workflow and should be removed or renamed in a later cleanup issue. |
| `remove in later cleanup issue` | Candidate for deletion after static tests and docs prove it is no longer needed. |
| `not recommended for new operator use` | May remain source-visible, but operators should choose one of the three primary profiles instead. |
| `source_safe` | Can be inspected in committed source without runtime mutation or external services. |
| `temporary_runtime_only` | May be used only in a deliberate live notebook copy with explicit gates and reviewed values. |
| `read_only_observation` | Displays bounded native or artifact observations without repairing, rewriting, or reinterpreting them. |

## Primary Profile Model

Notebook 14 has three primary operational profiles. `evidence_governance_preview`
is the sole committed default. All committed source defaults remain
preview-only; runtime actions require a profile that requests the action plus
explicit boolean gates and reviewed operator inputs.

| Profile | Status | Source-safe default status | Prerequisites | Permitted actions | Prohibited actions | Explicit gates | Required operator confirmations | Expected handoff outputs | Classification |
|---|---|---|---|---|---|---|---|---|---|
| `evidence_governance_preview` | Supported and committed default. | Sole default; no-write/no-execution. | None beyond valid notebook source. | Read source configuration, define helpers, compute disabled runtime controls, display intended command/review posture when executed without mutation. | Workspace initialization, Drive mount, archive restore, feature discovery/adoption, campaign input/config candidate creation, campaign execution, review-pack build/validation, governance report, catalog/lineage export, checkpoint creation, runtime summary writes. | All runtime gates remain false/unset; profile flags for init, drive, restore, campaign, review, governance, lineage, and checkpoint are false. | None. Real run IDs, review IDs, roots, archive IDs, paths, credentials, logs, and artifacts must not be committed. | No committed output. In a live preview execution, only in-memory diagnostics are expected. | `primary`, `source_safe` |
| `campaign_feature_restore_and_generation_run` | Supported first-run temporary-runtime path. | Not default; inert unless selected and gated. | Temporary runtime; reviewed archive/root values; explicit permission to initialize, mount Drive if needed, restore, discover/adopt feature roots, mark campaign inputs reviewed, and run native campaign. | Initialize native workspace/session, mount Drive only when explicitly allowed and needed, restore archive into an isolated target root, discover restored native feature artifacts, adopt a feature root only under gates, run native campaign preflight, run native research campaign, conservatively inspect resulting artifacts. | Governance decisions, promotion-state repair, review-pack canonicalization, ungated generated-config execution, unreviewed feature adoption, notebook fabrication of feature data, readiness or approval claims. | `NOTEBOOK14_ALLOW_STRATLAKE_INIT`, `RUN_STRATLAKE_INIT`, `NOTEBOOK14_ALLOW_DRIVE_MOUNT`, `NOTEBOOK14_ALLOW_ARCHIVE_RESTORE`, `RUN_ARCHIVE_RESTORE`, `NOTEBOOK14_DISCOVER_FEATURE_INPUTS`, `NOTEBOOK14_ALLOW_DISCOVERED_FEATURE_ROOT_ADOPTION`, `NOTEBOOK14_MARK_CAMPAIGN_INPUTS_USER_REVIEWED`, `NOTEBOOK14_ALLOW_NATIVE_CAMPAIGN_RUN`, `RUN_NATIVE_CAMPAIGN_GENERATION`, and generated-config gates when generated candidates are used. | Confirm archive source, isolated restore target, feature root adoption, campaign artifact root, campaign inputs, generated execution candidates if any, and no-use of committed real credentials or IDs. | Native command diagnostics, bounded artifact inventory, campaign preflight status, campaign result metadata, caveats, and optional runtime summary only when `NOTEBOOK14_WRITE_RUNTIME_SUMMARY=true`. | `primary`, `temporary_runtime_only` |
| `existing_campaign_evidence_governance_review` | Supported review-only continuation path and recommended review-only temporary-runtime path. | Not default; inert unless selected and gated. | Operator-confirmed existing campaign run identity and configured artifact root; optional reviewed review identity. | Initialize native workspace/session, select the existing confirmed run identity, build native derived evidence-review pack when absent, resolve pack root only under configured artifact root, run native strict validation, run native read-only governance report, optionally observe catalog/lineage. | Archive restore, Drive mount for archive restoration, campaign creation, execution-candidate work, campaign configuration generation, feature discovery/adoption, campaign-preparation caveats, borrowing campaign-generation state as review state, guessed run/review identities. | `NOTEBOOK14_ALLOW_STRATLAKE_INIT`, `RUN_STRATLAKE_INIT`, `NOTEBOOK14_ALLOW_EVIDENCE_REVIEW`, `RUN_EVIDENCE_REVIEW_PACK_BUILD`, `RUN_EVIDENCE_REVIEW_PACK_VALIDATE`, `NOTEBOOK14_ALLOW_EXISTING_EVIDENCE_PACK_VALIDATION`, `NOTEBOOK14_ALLOW_GOVERNANCE_REPORT`, `RUN_PROMOTION_GOVERNANCE_REPORT`, optional catalog/lineage gates. | Confirm selected run ID, optional review ID, campaign artifact root, pack overwrite policy, existing-pack validation permission, and catalog/lineage scope if used. | Native evidence build result, native strict validation result, display-only validation artifact observation, native read-only governance command result, bounded artifact classifications, caveats. | `primary`, `temporary_runtime_only`, `read_only_observation` |

## Legacy Profile Audit

Non-primary profiles remain visible in the staged notebook for compatibility
and lineage. They are not equivalent to the three recommended workflows.

| Profile | Status | Still supported | Temporary runtime use | Superseded by | Blending risk | Recommended disposition |
|---|---|---|---|---|---|---|
| `evidence_governance_preflight` | `retained compatibility mode`; `not recommended for new operator use`. | Source-retained. | Only for narrow workspace/session preflight with gates. | `evidence_governance_preview` for source-safe inspection, or a primary runtime profile for real work. | Low to moderate; initialization can be mistaken for review readiness. | Keep classified; add static assertion that preview remains the committed default. |
| `archive_restore_discovery` | `historical/reference example`; `not recommended for new operator use`. | Source-retained. | Only in a temporary runtime for archive restore discovery. | `campaign_feature_restore_and_generation_run`. | Moderate; restore/discovery without campaign ordering can leave ambiguous state. | Consolidate into the primary first-run template in a later cleanup issue. |
| `campaign_artifact_generation_run` | `retained compatibility mode`; `deprecated alias`. | Source-retained. | Temporary runtime only after reviewed campaign inputs. | `campaign_feature_restore_and_generation_run` when restore is needed, or a future campaign-only primary if one is explicitly designed. | Moderate; may create campaign artifacts without the documented restore/adoption sequence. | Mark as future cleanup candidate. |
| `campaign_evidence_governance_run` | `deprecated alias`; `remove in later cleanup issue`. | Source-retained but not recommended. | Avoid for new runs. | Split into `campaign_feature_restore_and_generation_run` followed by `existing_campaign_evidence_governance_review`. | High; blends campaign preparation/execution with review/governance surfaces. | Remove or replace with explicit two-phase operator handoff in a later issue. |
| `evidence_review_pack_build` | `retained compatibility mode`; `not recommended for new operator use`. | Source-retained. | Temporary runtime only for isolated native evidence-pack build. | `existing_campaign_evidence_governance_review`. | Low to moderate; can omit strict validation/governance context. | Keep classified; static tests should ensure pack roots stay under configured artifact root. |
| `governance_report_run` | `retained compatibility mode`; `not recommended for new operator use`. | Source-retained. | Temporary runtime only for native read-only governance reporting. | `existing_campaign_evidence_governance_review`. | Moderate; governance output without confirmed review-pack context can be misread. | Keep classified; require read-only language and no promotion claims. |
| `catalog_lineage_review` | `retained compatibility mode`; `historical/reference example`. | Source-retained. | Temporary runtime only for optional catalog/lineage observation. | Optional catalog/lineage step inside `existing_campaign_evidence_governance_review`. | Low; still must not be treated as governance evidence. | Keep classified; future tests should assert catalog/lineage classification is observational. |
| `evidence_governance_full_review` | `deprecated alias`; `remove in later cleanup issue`. | Source-retained but not recommended. | Avoid for new runs. | The two primary runtime phases with an explicit handoff between them. | High; combines Drive, restore, review, governance, lineage, and checkpoint intent. | Simplify or remove after Issue #143 static assertions protect the primary model. |

## Override-Template Inventory

All committed override examples remain commented and inactive. A source-safe
Notebook 14 must not contain real Drive paths, local user paths, run IDs,
review IDs, archive IDs, credentials, artifact inventories, logs, execution
summaries, generated review packs, governance reports, or checkpoints.

| Notebook block | Template classification | Recommended use | Superseded or duplicate surface | Future cleanup |
|---|---|---|---|---|
| Cell 5 review-only continuation block | `current source-safe template` for review-only evidence/governance work. | Use as the recommended starting point for `existing_campaign_evidence_governance_review` in a temporary copy after substituting reviewed placeholders. | Overlaps cells 7, 9, and 10. | Consolidate duplicate review-only examples into one documented template. |
| Cell 6 restore/discover/campaign block | `current source-safe template` for first-run restore/campaign sequence. | Use as the recommended starting point for `campaign_feature_restore_and_generation_run` in a temporary copy after substituting reviewed placeholders. | Overlaps cells 11 and 12 restore/campaign examples. | Keep as the primary first-run template; remove narrower duplicates later. |
| Cell 7 historical review capture | `historical retained example`; `do not use for new runs`. | Lineage only. | Superseded by cell 5 and this document. | Remove after static tests cover review-only gates. |
| Cell 8 campaign-generation fragment | `deprecated example`; `do not use for new runs`. | None for new runs; it lacks full profile/root context. | Superseded by cell 6. | Remove or merge into the primary first-run template. |
| Cell 9 `campaign_evidence_governance_run` block | `deprecated example`; `do not use for new runs`. | Avoid; it blends campaign/review/governance intent under a legacy profile. | Superseded by the primary two-phase model. | Remove after Issue #143 asserts review-only exclusions. |
| Cell 10 compact review-only block | `temporary runtime-only example`; duplicate of current template. | Acceptable as a short reviewed-run continuation snippet, but cell 5 is the recommended template. | Duplicates cell 5. | Consolidate with cell 5. |
| Cell 11 minimal restore/campaign block | `historical/reference example`; incomplete for new runs. | Reference only; it does not contain all recommended gates. | Superseded by cell 6. | Remove or fold into cell 6. |
| Cell 12 smoke/legacy multi-profile block | `historical retained example`; includes deprecated/future-cleanup profiles. | Reference only for legacy smoke patterns and primary profile lineage. | Superseded by cells 5 and 6 plus the profile matrix above. | Split current templates from historical examples or remove legacy snippets in a later cleanup issue. |
| Cells 25-28 runtime-only inspection snippets | `temporary runtime-only example`; historical inspection helpers. | Use only after explicit native outputs exist in a temporary runtime. | Not profile templates. | Keep or move to a companion runtime guide if they remain useful. |

## M45 Promotion-State And Governance Boundaries

Notebook 14 preserves these ownership rules:

- Review promotion state is review-owned.
- Campaign promotion state is campaign-owned.
- Canonical promotion-state construction, serialization, validation, and
  emission are engine-owned.
- Notebook governance is observational and read-only.
- Notebook parsing is bounded, display-oriented, non-authoritative, and
  non-repairing.

Notebook 14 must not create, backfill, repair, normalize, or rewrite canonical
`promotion_gates.json`; must not replay policy or gate evaluation; treat a derived
evidence-review pack as canonical governance evidence; must not borrow review
promotion state as campaign promotion state; must not borrow campaign promotion
state as review promotion state; or treat `not_reviewed` as eligibility, approval, promotion,
readiness, deployment suitability, production suitability, or live-trading
suitability.

For the canonical no-policy condition:

```text
configured = false
configuration_state = not_configured
evaluation_status = not_configured
promotion_status = not_reviewed
decision_authority = none
```

Notebook 14 must use this wording exactly:

```text
No promotion policy was configured; no promotion decision was made.
```

Missing and malformed canonical evidence remain integrity observations. No
notebook fallback, repair, normalization, or reinterpretation may occur.

## Artifact Classification

Notebook 14 uses bounded, read-only artifact classifications to prevent
runtime material from being mistaken for canonical governance evidence.

| Classification | Meaning | Boundary |
|---|---|---|
| `canonical_engine_owned_promotion_state_candidate` | Exact-filename `promotion_gates.json` candidate discovered by bounded inspection. | Display-only candidate; engine validation and native governance output remain authoritative. |
| `native_governance_output_candidate` | Native governance report output candidate. | Read-only observation; not notebook-generated promotion evidence. |
| `derived_evidence_review_pack_non_authoritative` | Native derived evidence-review pack artifact. | Non-authoritative for governance; must not be copied, moved, rewritten, normalized, repaired, or treated as canonical promotion state. |
| `catalog_or_lineage_observability_artifact` | Catalog or lineage output used for observability. | Observational only; not governance evidence. |
| `restored_feature_or_qa_artifact_non_governance` | Restored feature or QA artifact found after archive restore. | Input/QA context only; not campaign approval or governance evidence. |
| `notebook_runtime_noncanonical_excluded` | Notebook-local runtime output under `_notebook_14_runtime` or equivalent notebook namespace. | Excluded from reviewable evidence discovery. |
| `unknown_or_unclassified_artifact` | Artifact that does not match a known source-safe class. | Must remain conservative and non-authoritative until classified by later work. |

The exact-filename `promotion_gates.json` inspection remains bounded,
read-only, and runtime-namespace-excluding. Runtime artifacts under
`_notebook_14_runtime` are noncanonical and excluded. Derived review packs,
catalog/lineage output, and restored feature/QA artifacts do not become
canonical governance evidence through notebook discovery.

## Derived Review Pack Guardrails

Derived evidence-review packs are review artifacts only. They are classified as
`derived_evidence_review_pack_non_authoritative` and remain non-authoritative
for promotion governance. Notebook 14 must not treat a derived review pack as
canonical promotion-state evidence, synthesize or backfill missing canonical
evidence from pack contents, infer promotion eligibility or decision status
from a pack, or copy, move, normalize, repair, rewrite, or mutate derived
review-pack JSON.

The default evidence-review repository root convention remains:

```text
EVIDENCE_REVIEW_REPO_ROOT = CAMPAIGN_ARTIFACT_ROOT.parent
```

When a native command reports a repository-relative pack root, Notebook 14
resolves it relative to `EVIDENCE_REVIEW_REPO_ROOT`, canonicalizes the resolved
path, and accepts it only when it remains under `CAMPAIGN_ARTIFACT_ROOT`.
Repository-relative output roots must not be resolved against the notebook
process working directory. A reported pack root outside the configured artifact
root remains an integrity caveat; Notebook 14 must not create a fallback root
outside the configured artifact tree.

Existing-pack discovery is bounded by `NOTEBOOK14_EXISTING_EVIDENCE_PACK_DISCOVERY_LIMIT`,
confined to `CAMPAIGN_ARTIFACT_ROOT`, and excludes notebook runtime namespaces
such as `_notebook_14_runtime`. The limit bounds inspected filesystem entries,
not merely matching candidates returned. A runtime-namespace entry counts as
inspected once reached and is then excluded without recursion. Discovery may be
incomplete when the scan truncates.

Automatic existing-pack resolution is permitted only when exactly one valid
matching candidate exists after a non-truncated bounded scan. Zero candidates
remain a conservative `no_existing_pack_found` outcome. Multiple matching
candidates remain a `multiple_existing_packs_require_operator_selection`
outcome. Truncated discovery remains an
`existing_pack_discovery_truncated_requires_operator_selection` outcome even
when one matching candidate was found before the limit. Ambiguity or truncation
requires operator selection through `NOTEBOOK14_REVIEW_ID` or an explicitly
reviewed higher inspection limit. Unknown or unclassified candidates are not
treated as review packs, and discovery must not copy, relocate, rewrite, or
mutate candidates.

Existing packs are preserved by default. `NOTEBOOK14_ALLOW_EVIDENCE_REVIEW_PACK_OVERWRITE`
defaults to false and is separate from `NOTEBOOK14_ALLOW_EXISTING_EVIDENCE_PACK_VALIDATION`.
Building a new pack must not silently overwrite an existing pack. Rebuilding,
overwriting, or validating an existing pack requires explicit runtime gates,
and preview mode must not discover, validate, overwrite, or build packs.

## Native Command Authority

The following native surfaces are authoritative only when explicitly gated and
run in a temporary environment:

- native campaign preflight and campaign execution;
- native evidence-review pack build;
- native strict validation;
- native read-only governance report;
- optional catalog/lineage observation.

Notebook 14 may collect bounded diagnostics for command text, executed/skipped
state, return code, bounded stdout/stderr tails, selected run/catalog/review
identity, effective roots, and display-only observation of engine-written
`validation.json`.

Notebook 14 must not become replacement validation, policy interpretation,
artifact repair, or a workaround for native command failures.

## Native Validation Caveat

A native evidence-review pack build may succeed while native strict validation
reports invalid schema-governed review-pack JSON files. Treat that condition as
an engine-owned package, contract-resource, validator, or version-compatibility
follow-up until verified in `christophermoverton/stratlake-trade-engine`.

The notebook repository must not copy engine contract schemas, rewrite or
normalize review-pack JSON, bypass strict validation, replace native
validation, weaken native failure results, or assert an unverified root cause.
Notebook 14 may record the condition only as a bounded operational caveat.
When native strict validation reports a failure, the conservative handoff is:

```text
Native strict validation reported a failure; Notebook 14 did not repair, bypass, or reinterpret the native result.
```

## Issue #143 Static-Test Handoff

Issue #143 should add static assertions for the following Notebook 14
boundaries:

- The committed default remains `evidence_governance_preview`.
- Preview profile flags for init, Drive, restore, campaign, review,
  governance, lineage, and checkpoint remain false.
- Runtime allow gates and `RUN_*` gates remain disabled by committed source.
- Code-cell outputs are empty and execution counts are null.
- Active runtime override assignments, active install commands, real Drive
  paths, local user paths, run IDs, review IDs, archive IDs, credentials,
  logs, and generated artifacts are absent from committed source.
- The three primary profile names are present and documented:
  `evidence_governance_preview`,
  `campaign_feature_restore_and_generation_run`, and
  `existing_campaign_evidence_governance_review`.
- Review-only mode excludes archive restoration, Drive archive restore,
  campaign generation, execution-candidate config creation, feature
  discovery/adoption, and campaign-preparation caveats.
- Legacy profiles are explicitly classified and are not documented as
  recommended primary workflows.
- `EVIDENCE_REVIEW_REPO_ROOT = CAMPAIGN_ARTIFACT_ROOT.parent` remains the
  default convention, and repository-relative native output roots resolve
  under the configured campaign artifact root.
- Derived evidence-review packs are not copied, moved, rewritten, repaired, or
  treated as canonical governance evidence.
- Exact-filename `promotion_gates.json` inspection remains bounded,
  read-only, runtime-namespace-excluding, and display-only.
- The no-policy wording remains exactly:
  `No promotion policy was configured; no promotion decision was made.`
- Review-owned and campaign-owned promotion states are not merged or borrowed.
- `not_reviewed` is not described as eligibility, approval, promotion,
  readiness, deployment suitability, production suitability, or live-trading
  suitability.
- `_notebook_14_runtime` artifacts are classified as noncanonical and excluded
  from reviewable evidence discovery.
- Native strict-validation failures remain native failures; the notebook does
  not provide fallback validation, schema copying, JSON repair, or root-cause
  assertions.

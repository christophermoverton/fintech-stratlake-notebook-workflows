# Notebook 12 Staging Classification

## Purpose

This document records the repository staging posture for Notebook 12 after
Issue #117 / M15.1 and the runtime/campaign/evidence surface classification
posture completed in Issue #118 / M15.2.

Notebook 12 is the StratLake campaign evidence gap and promotion-readiness
review continuation after Notebook 11. It reviews whether campaign-level native
artifacts can support a conservative human-review handoff. It is not native
StratLake campaign orchestration, strategy approval, alpha validation,
production-readiness certification, or promotion governance.

This document is source-only. It does not execute notebook cells, install
packages, mount Drive, restore archives, initialize sessions, run campaigns,
run governance jobs, write artifacts, checkpoint archives, or make
promotion-grade claims.

## Import Candidate

| Property | Value |
|---|---|
| Source artifact | `Notebook_12_Stratlake_Campaign_Evidence_Gap_and_Promotion_Readiness_RESEARCH_DRAFT_with_handoff_next_action_precision (4).ipynb` |
| Target path | `notebooks/12_stratlake_campaign_evidence_gap_promotion_readiness.ipynb` |
| Source notebook shape | 50 cells: 29 markdown, 21 code |
| Repository role | Cleaned, output-free, source-safe notebook source |
| Committed default profile | `cold_smoke_5_command_shape_readiness` |
| Baseline preview profile | `cold_smoke_1_preview` |
| Manual smoke mode | `campaign_smoke_run` |

## Source-Safe Staging Result

| Source-safety property | Result |
|---|---|
| Notebook staged at target path | Yes |
| Outputs cleared | Yes; code cells have no outputs |
| Execution counts reset | Yes; execution counts are null |
| Cell IDs removed | Yes |
| Top-level metadata minimized | Yes; limited to `kernelspec` and `language_info` |
| Runtime artifacts committed | No |
| Notebook cells executed during staging | No |
| Promotion-grade claim made during staging | No |

## Guarded Controls

Notebook 12 defaults to source-safe command-shape readiness:

```python
NOTEBOOK12_TEST_PROFILE = "cold_smoke_5_command_shape_readiness"
RUN_NATIVE_CAMPAIGN_SMOKE = False
ALLOW_NATIVE_CAMPAIGN_SMOKE_EXECUTION = False
NATIVE_CAMPAIGN_SMOKE_DRY_RUN_ONLY = True
REQUIRE_DRY_RUN_ARGUMENT_FOR_NATIVE_CAMPAIGN_SMOKE = True
ALLOW_NON_DRY_RUN_NATIVE_CAMPAIGN_SMOKE_EXECUTION = False
ALLOW_PROVISIONAL_CAMPAIGN_SMOKE_CONFIG_FOR_EXECUTION = False
VALIDATE_PROVISIONAL_CAMPAIGN_SMOKE_CONFIG = True
RUN_ID_STRICT_PLATFORM_ARTIFACT_DISCOVERY = True
```

`cold_smoke_1_preview` remains available as the baseline no-restore preview
profile, but the committed import default is
`cold_smoke_5_command_shape_readiness`. This clarification fixes the M15.1
audit mismatch without weakening execution guards.

Dry-run and provisional boundaries remain explicit:

- `campaign_smoke_preview` previews only and does not execute.
- `campaign_smoke_dry_run` requires execution enablement and an advertised
  native dry-run argument.
- `campaign_smoke_dry_run_allow_provisional` may use a validated
  `notebook12_generated_smoke_config`, but still remains dry-run only.
- `campaign_smoke_execute_allow_provisional_no_dry_run` is the only named
  non-dry-run smoke profile and should be used deliberately only after preview
  and dry-run audits.

## Runtime Surfaces

The detailed reusable surface matrix lives in
[Notebook 12 command surface classification](notebook_12_command_surface_classification.md).
The staging-level summary is:

| Surface | Classification | Default/source posture |
|---|---|---|
| Dependency installation | `live_manual`, `out_of_ci_scope` | Source reference only |
| Imports, Colab detection, display helpers | `source_only`, `runtime_validation` | Source-inspectable helpers |
| Runtime controls and profiles | `source_only`, `guarded_runtime` | Default is command-shape readiness with execution disabled |
| Colab, Drive, workspace setup | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Manual runtime only |
| Session archive root discovery | `runtime_validation`, `artifact_review` | Optional paths |
| CLI/import availability checks | `runtime_validation`, `preview_only` | Command/help shape only |
| Fintech session initialization | `live_manual`, `guarded_runtime`, `runtime_validation` | Manual runtime only |
| StratLake session initialization | `live_manual`, `guarded_runtime`, `runtime_validation` | Manual runtime only |
| Guarded native campaign smoke path | `preview_only`, `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Off unless explicit profile/controls allow it |
| Generated provisional smoke config | `artifact_review`, `guarded_runtime`, `runtime_validation`, `out_of_ci_scope` | Classified as `notebook12_generated_smoke_config` |
| Dry-run detection and blocking | `guarded_runtime`, `runtime_validation` | Blocks when dry-run support is missing |
| Optional archive restore | `live_manual`, `guarded_runtime`, `artifact_review`, `out_of_ci_scope` | Off by default |
| Notebook 11 context discovery | `runtime_validation`, `artifact_review`, `campaign_evidence_review` | Context only, not native campaign proof |
| Campaign artifact discovery | `artifact_review`, `runtime_validation`, `campaign_evidence_review` | Missing artifacts become caveats |
| Native campaign artifact filtering | `artifact_review`, `runtime_validation`, `campaign_evidence_review` | Strict native/review artifact distinction |
| Notebook 12 review artifact separation | `artifact_review`, `campaign_evidence_review` | Review rows do not fabricate native context |
| Campaign evidence dataframe | `artifact_review`, `campaign_evidence_review` | Human-review sufficiency labels only |
| Governance/evidence/report command previews | `preview_only`, `runtime_validation`, `guarded_runtime` | Preview/manual schema posture |
| Caveat register | `campaign_evidence_review`, `artifact_review` | Missing evidence remains visible |
| Notebook 12 review artifact writing | `artifact_review`, `out_of_ci_scope` | Runtime outputs only; not committed |
| Optional archive checkpoint | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Off by default |
| Final handoff | `source_only`, `artifact_review`, `campaign_evidence_review` | Conservative next-action summary |

## Expected Artifact Path

Generated runtime outputs are expected under:

```text
artifacts/notebook_12_campaign_evidence_gap_promotion_readiness/
```

Generated smoke configs, review CSVs, summaries, handoffs, restored archives,
runtime workspaces, Drive folders, reports, logs, checkpoints, notebook outputs,
and execution counts remain outside Git.

## Evidence Interpretation

Notebook 12 preserves three source-safe boundaries:

- Native campaign artifacts remain distinct from Notebook 12 review artifacts.
  `native_campaign_artifact_rows`, `notebook12_review_artifact_rows`, and
  `candidate_campaign_context_rows` should not be collapsed into a fabricated
  campaign context.
- Generated smoke configs are useful for preview and explicitly guarded smoke
  tests, but their source remains `notebook12_generated_smoke_config`, not a
  native campaign template.
- Missing campaign context, missing split metrics, missing promotion gates, or
  missing promotion evidence are caveats and blockers. They are not success
  statuses.

The final handoff may recommend restoring a campaign archive, supplying a true
native campaign template, running a guarded dry-run smoke, or rerunning evidence
review after artifacts exist. It must not approve strategies or certify
promotion readiness.

## Non-Claims

Notebook 12 source must not claim native orchestration coverage, strategy
approval, alpha validation, production readiness, statistical significance,
promotion governance success, or promotion-grade readiness. Repository source
import is not runtime proof, and CI validation is not Colab/manual runtime
equivalence.

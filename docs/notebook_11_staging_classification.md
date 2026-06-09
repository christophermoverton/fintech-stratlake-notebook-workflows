# Notebook 11 Staging Classification

## Purpose

This document records the repository staging posture for Notebook 11 after
Issue #109 / M14.1.

Notebook 11 is the StratLake expanded promotion evidence review continuation
after Notebook 10. Its theme is "from confidence review to promotion evidence."
It reviews evidence sufficiency, caveats, blockers, and promotion-readiness
interpretation. It is not a new promotion engine and it is not a renamed
Notebook 10.

This document is source-only. It does not execute notebook cells, install
packages, mount Drive, restore archives, initialize sessions, run strategies,
run governance jobs, write artifacts, checkpoint archives, or make
promotion-grade claims.

## Import Candidate

| Property | Value |
|---|---|
| Source artifact | `Notebook_11_Stratlake_Expanded_Promotion_Evidence_Review_STANDALONE_DRAFT_v17_REFERENCE_CONTEXT_AUDITED (1).ipynb` |
| Companion document | `notebook_11_companion_importation_document_for_m14.md` |
| Target path | `notebooks/11_stratlake_expanded_promotion_evidence_review.ipynb` |
| Source notebook shape | 51 cells: 28 markdown, 23 code |
| Repository role | Cleaned, output-free, source-safe notebook source |
| Default mode | `expanded_preview` |
| Manual runtime mode | `expanded_run` |

## Source-Safe Staging Result

| Source-safety property | Result |
|---|---|
| Notebook staged at target path | Yes |
| Outputs cleared | Yes; code cells have no outputs |
| Execution counts reset | Yes; execution counts are null |
| Cell IDs removed | Yes |
| Top-level metadata minimized | Yes; limited to `kernelspec` and `language_info` |
| Drive folder placeholder guarded | Yes; `REPLACE_WITH_DRIVE_FOLDER_NAME` guard retained |
| Runtime artifacts committed | No |
| Notebook cells executed during staging | No |
| Promotion-grade claim made during staging | No |

## Guarded Controls

Notebook 11 defaults to source-safe preview behavior:

```python
NOTEBOOK11_MODE = "expanded_preview"
RUN_STRATLAKE_ARCHIVE_RESTORE = False
RUN_EXPANDED_STRATEGY_EVALUATION = False
ALLOW_MANUAL_REVIEW_CANDIDATE_RUNS = False
ALLOW_REFERENCE_ONLY_EXPANDED_PLAN = False
RUN_PROMOTION_GOVERNANCE_REPORT = False
RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False
DISCOVER_EXISTING_EXPANDED_PLATFORM_ARTIFACTS = False
AUTO_RESTORE_NOTEBOOK10_CONTEXT_IF_MISSING = False
RUN_EVIDENCE_REVIEW_CLI_BUILD = False
RUN_PROMOTION_GOVERNANCE_REPORT_CLI = False
RUN_ID_STRICT_PLATFORM_ARTIFACT_DISCOVERY = True
```

`expanded_run` remains documented and supported, but it is manual. A user must
explicitly review the expanded plan and then enable strategy execution and
manual-review candidate runs. Archive restore remains separately guarded so
Notebook 10 artifacts are restored only when intentionally needed.

## Runtime Surfaces

| Surface | Classification | Default/source posture |
|---|---|---|
| Package installation | `live_manual`, `out_of_ci_scope` | Source reference only |
| Colab and Google Drive auth | `live_manual`, `guarded_runtime` | Placeholder guarded |
| Alpaca credentials | `live_manual`, `guarded_runtime` | Names only; values not committed |
| Fintech session initialization | `live_manual`, `guarded_runtime` | Notebook 10-style pattern preserved |
| StratLake session initialization | `live_manual`, `guarded_runtime` | `--notebook-configs` pattern preserved |
| Notebook 10 archive restore | `live_manual`, `guarded_runtime` | Off by default |
| Expanded strategy evaluation | `live_manual`, `guarded_runtime` | Off by default |
| Manual-review candidate execution | `live_manual`, `guarded_runtime` | Off by default |
| Governance/evidence-review execution | `live_manual`, `guarded_runtime` | Off by default |
| Existing expanded artifact discovery | `artifact_review`, `guarded_runtime` | Off by default |
| Notebook 11 review packages | `artifact_review` | Runtime outputs only; not committed |
| Archive checkpoint | `live_manual`, `guarded_runtime` | Off by default |

## Expected Artifact Path

Generated runtime outputs are expected under:

```text
artifacts/notebook_11_expanded_promotion_evidence_review/
```

Generated outputs, restored archives, strategy artifacts, reports, plots,
logs, checkpoints, notebook outputs, and execution counts remain outside Git.

## Evidence Interpretation

The imported source preserves two review paths:

- Source-safe/reference-only expanded preview: no archive restore, no expanded
  execution, no fabricated expanded candidate rows, and the handoff status
  `expanded_preview_reference_only_context_needs_notebook10_artifacts` when
  Notebook 10 artifacts are unavailable.
- Manual artifact-backed expanded run: explicitly enabled runtime execution for
  the manual-review candidates `buy_and_hold_v1`,
  `cross_section_momentum`, `seeded_random_v1`, and `sma_crossover_v1`.

The raw audit reported successful expanded command execution and metric loading
for the manual candidates, but complete promotion evidence remains incomplete
where split metrics and promotion-gate artifacts are absent. Repository source
import does not prove runtime execution.

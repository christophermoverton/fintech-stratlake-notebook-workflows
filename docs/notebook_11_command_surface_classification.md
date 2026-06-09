# Notebook 11 Command Surface Classification

## Purpose

Notebook 11 (`notebooks/11_stratlake_expanded_promotion_evidence_review.ipynb`)
is a source-safe expanded evidence sufficiency review notebook. It composes
existing Fintech and StratLake surfaces to review Notebook 10 evidence, preview
expanded evidence needs, and optionally run artifact-backed expanded validation
when a user deliberately enables runtime gates.

This classification does not prove live package installation, Drive access,
credential availability, archive restore, strategy success, artifact
completeness, checkpoint success, production readiness, strategy approval,
statistical significance, alpha, complete platform artifact coverage,
CI/runtime equivalence, or promotion-grade evidence.

## Source And Runtime Posture

| Property | Value |
|---|---|
| Target notebook | `notebooks/11_stratlake_expanded_promotion_evidence_review.ipynb` |
| Source posture | Cleaned, output-free, execution-count-null, metadata-minimized |
| Runtime posture | Live/manual Colab or prepared local notebook execution only |
| Default mode | `expanded_preview` |
| Manual runtime mode | `expanded_run` |

## Classification Legend

| Category | Meaning |
|---|---|
| `source_only` | Source text, notebook JSON, metadata, references, and guards can be inspected without runtime execution. |
| `live_manual` | Requires deliberate live notebook execution in Colab or another prepared runtime. |
| `guarded_runtime` | Runtime action is protected by a mode switch, boolean gate, placeholder guard, or manual enablement. |
| `runtime_validation` | Depends on restored paths, configs, CLI availability, or generated runtime rows. |
| `artifact_review` | Discovers, writes, inventories, or interprets generated runtime artifacts. |
| `promotion_readiness_review` | Interprets evidence sufficiency and blockers without approving strategies. |
| `out_of_ci_scope` | Must not be required by repository validation or CI. |

## Command And Runtime Surfaces

| Surface | Notebook use | Classification | Source-only validation boundary |
|---|---|---|---|
| Package installation | Installs `pandas-market-calendars`, `fintech-market-ingestion`, and `stratlake-trade-engine` in live runtime using the TestPyPI + PyPI fallback pattern. | `live_manual`, `out_of_ci_scope` | Verify install command shape only; do not install packages in repository validation. |
| Colab and Google Drive mount | Mounts Drive when running in Colab and uses `DRIVE_FOLDER_NAME = "REPLACE_WITH_DRIVE_FOLDER_NAME"` as the committed placeholder. | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Verify placeholder guard only; do not mount Drive. |
| Optional Alpaca credentials | Keeps Notebook 10 parity for live data-access validation paths. | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Verify credential names only; no values committed; no prompts in CI. |
| Fintech session initialization: `fintech-init-project` | Creates or attaches the Fintech project/session structure before StratLake review. | `live_manual`, `guarded_runtime`, `runtime_validation` | Verify command construction only; do not initialize sessions in CI. |
| StratLake session initialization: `stratlake-init-session` | Creates or attaches the StratLake session with notebook configs before restore/review. | `live_manual`, `guarded_runtime`, `runtime_validation` | Verify command construction only; preserve the Notebook 10-style `--notebook-configs` pattern. |
| Notebook 10 archive restore: `stratlake-session-archive-restore-bootstrap` | Restores Notebook 10 context only when intentionally enabled or manually requested. | `live_manual`, `guarded_runtime`, `artifact_review`, `out_of_ci_scope` | Verify restore command shape and false default; do not restore archives in tests. |
| Notebook 10 artifact/context discovery | Loads or probes Notebook 10 `summary.json`, `smoke_audit_summary.json`, `promotion_review`, `artifact_inventory`, `walk_forward_results`, `robustness_summary`, and `preflight_summary`. | `runtime_validation`, `artifact_review`, `promotion_readiness_review` | Verify expected paths and fallback behavior; do not require files to exist during repository validation. |
| Reference-summary fallback | Provides source-safe Notebook 10 context when runtime artifacts are unavailable. | `source_only`, `promotion_readiness_review` | Confirm fallback is context only and does not fabricate expanded candidate rows by default. |
| Expanded strategy execution: `stratlake-run-strategy` | Executes expanded strategy/window commands only when `RUN_EXPANDED_STRATEGY_EVALUATION` is enabled. | `live_manual`, `guarded_runtime`, `runtime_validation`, `out_of_ci_scope` | Verify command shape only, including `--strategies-config`, `--strategy`, `--start`, and `--end`; do not execute strategies. |
| Manual-review candidate runs | Allows `buy_and_hold_v1`, `cross_section_momentum`, `seeded_random_v1`, and `sma_crossover_v1` only when manual-review gates are enabled. | `live_manual`, `guarded_runtime`, `runtime_validation` | Verify candidate names and gates; do not execute candidates. |
| Expanded artifact discovery | Discovers metric artifacts, run-id strict platform artifacts, explicitly enabled existing expanded artifacts, and strategy/run-id fallback matches. | `artifact_review`, `runtime_validation`, `promotion_readiness_review` | Verify flags and path references; do not require generated artifacts. |
| Notebook 11 interpretive review packages | Writes notebook-scoped review packages when expanded-run metrics exist but platform split/readiness/gate artifacts are incomplete. | `artifact_review`, `promotion_readiness_review`, `out_of_ci_scope` | Verify generated path only; do not commit generated packages; these are review aids, not replacements for upstream StratLake promotion-engine outputs. |
| Governance/evidence-review CLI schema discovery | Checks `stratlake-build-evidence-review build --help` and `stratlake-run-promotion-governance-report --help` when manually enabled for schema review. | `live_manual`, `guarded_runtime`, `runtime_validation` | Help/schema discovery may be safe in manual runtime, but is not required for CI/source validation. |
| Governance/evidence-review CLI execution | Optionally runs `stratlake-build-evidence-review` and `stratlake-run-promotion-governance-report` after schema surfaces are understood. | `live_manual`, `guarded_runtime`, `artifact_review`, `promotion_readiness_review`, `out_of_ci_scope` | Verify false defaults; do not execute governance commands in tests. |
| Caveat/blocker register | Records missing Notebook 10 artifacts, disabled expanded execution, missing metrics readiness, missing split metrics, missing promotion gates, and governance gaps. | `promotion_readiness_review`, `artifact_review` | Verify conservative language; missing split metrics and promotion gates remain caveats/blockers, not hidden successes. |
| Notebook 11 artifact writing | Writes source-visible review outputs under `artifacts/notebook_11_expanded_promotion_evidence_review/`. | `artifact_review`, `out_of_ci_scope` | Verify path only; generated outputs stay out of Git. |
| Archive checkpoint: `stratlake-session-archive-bootstrap` | Optionally checkpoints runtime state after Notebook 11 review. | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Verify false default and command shape; do not checkpoint in tests. |

## Guarded Controls

Notebook 11 source defaults remain conservative:

```python
NOTEBOOK11_MODE = os.environ.get("NOTEBOOK11_MODE", "expanded_preview")
RUN_STRATLAKE_ARCHIVE_RESTORE = env_bool("RUN_STRATLAKE_ARCHIVE_RESTORE", False)
RUN_EXPANDED_STRATEGY_EVALUATION = env_bool("RUN_EXPANDED_STRATEGY_EVALUATION", False)
ALLOW_MANUAL_REVIEW_CANDIDATE_RUNS = env_bool("ALLOW_MANUAL_REVIEW_CANDIDATE_RUNS", False)
ALLOW_REFERENCE_ONLY_EXPANDED_PLAN = env_bool("ALLOW_REFERENCE_ONLY_EXPANDED_PLAN", False)
RUN_PROMOTION_GOVERNANCE_REPORT = env_bool("RUN_PROMOTION_GOVERNANCE_REPORT", False)
RUN_STRATLAKE_ARCHIVE_CHECKPOINT = env_bool("RUN_STRATLAKE_ARCHIVE_CHECKPOINT", False)
DISCOVER_EXISTING_EXPANDED_PLATFORM_ARTIFACTS = env_bool("DISCOVER_EXISTING_EXPANDED_PLATFORM_ARTIFACTS", False)
AUTO_RESTORE_NOTEBOOK10_CONTEXT_IF_MISSING = env_bool("AUTO_RESTORE_NOTEBOOK10_CONTEXT_IF_MISSING", False)
RUN_EVIDENCE_REVIEW_CLI_BUILD = env_bool("RUN_EVIDENCE_REVIEW_CLI_BUILD", False)
RUN_PROMOTION_GOVERNANCE_REPORT_CLI = env_bool("RUN_PROMOTION_GOVERNANCE_REPORT_CLI", False)
RUN_ID_STRICT_PLATFORM_ARTIFACT_DISCOVERY = env_bool("RUN_ID_STRICT_PLATFORM_ARTIFACT_DISCOVERY", True)
```

`expanded_preview` defensively disables expanded execution, governance report
execution, evidence-review CLI build, promotion-governance CLI execution, and
archive checkpointing. `review_only` applies the same runtime side-effect
shutdown and also disables manual-review candidate runs.

## Source-Only Validation Boundary

Repository validation may inspect notebook JSON, source text, default controls,
command strings, path references, manual candidate names, non-claim language,
and expected artifact paths.

Repository validation must not execute notebook cells, install packages, mount
Google Drive, prompt for credentials, initialize Fintech or StratLake sessions,
restore archives, run strategies, run governance jobs, write artifacts, create
checkpoint archives, or treat source import as runtime proof.

## Manual Runtime Validation Boundary

Manual runtime validation may, when explicitly enabled, install packages,
initialize Fintech and StratLake session structure, restore Notebook 10
artifacts, preview expanded candidates, run selected manual-review candidates,
load metrics, write Notebook 11 interpretive review packages, inspect
governance/evidence-review CLI schemas, optionally run governance/evidence-review
CLI commands, and optionally checkpoint the resulting runtime state.

## Manual Candidates

Expanded-run manual-review candidates are source-visible and guarded:

- `buy_and_hold_v1`
- `cross_section_momentum`
- `seeded_random_v1`
- `sma_crossover_v1`

Command success and metric availability for these candidates are raw audit
context only until rerun in a live runtime. Missing split metrics and promotion
gate artifacts remain evidence blockers.

## Evidence Caveats

- Command success is not promotion-grade evidence by itself.
- Metric loading is useful but incomplete without split metrics and promotion
  gates.
- Notebook 11 interpretive packages are notebook-scoped review aids only.
- Platform split metrics and promotion gates remain required for complete
  promotion evidence.
- Source import is not runtime proof.
- CI validation is not Colab/manual runtime equivalence.
- Notebook 11 does not approve strategies.

## Non-Claims

Notebook 11 source must not claim alpha, production readiness, strategy
approval, statistical significance, complete platform artifact coverage,
CI/runtime equivalence, archive/checkpoint generality, or promotion-grade
evidence. It should frame results as expanded evidence review,
caveat/blocker review, and promotion-readiness interpretation.

# Notebook 11 Command Surface Classification

## Purpose

Notebook 11 (`notebooks/11_stratlake_expanded_promotion_evidence_review.ipynb`)
is a source-safe expanded evidence sufficiency review notebook. It composes
existing Fintech and StratLake surfaces to review Notebook 10 evidence, preview
expanded evidence needs, and optionally run artifact-backed expanded validation
when a user deliberately enables runtime gates.

This classification does not prove live package installation, Drive access,
credential availability, archive restore, strategy success, artifact
completeness, checkpoint success, production readiness, statistical
significance, alpha, or promotion-grade evidence.

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
| Package installation | Installs `pandas-market-calendars`, `fintech-market-ingestion`, and `stratlake-trade-engine` in live runtime. | `live_manual`, `out_of_ci_scope` | Verify package references only; do not install. |
| Colab/Drive auth | Mounts Drive when running in Colab. | `live_manual`, `guarded_runtime` | Verify placeholder guard only. |
| Alpaca credentials | Optional credential parity with prior notebooks. | `live_manual`, `guarded_runtime` | Verify names only; no values or prints. |
| `fintech-init-project` | Initializes or attaches Fintech project/session. | `live_manual`, `guarded_runtime` | Verify command construction only. |
| `stratlake-init-session` | Initializes or attaches StratLake session with notebook configs. | `live_manual`, `guarded_runtime` | Verify command construction only. |
| `stratlake-session-archive-restore-bootstrap` | Restores Notebook 10 context when intentionally enabled. | `live_manual`, `guarded_runtime` | Confirm false default and source command shape. |
| Notebook 10 artifact discovery | Loads handoff, promotion review, smoke audit, and artifact inventory context. | `runtime_validation`, `artifact_review` | Verify paths and reference-only fallback behavior. |
| `stratlake-run-strategy` | Executes expanded strategy/window commands only when gates are enabled. | `live_manual`, `guarded_runtime` | Verify `--strategies-config`, `--strategy`, `--start`, and `--end` references only. |
| Expanded metric loading | Loads metrics for expanded-run candidates when generated or restored. | `artifact_review` | Verify source fields only; do not require files. |
| Governance/evidence-review CLI | Optional schema discovery and guarded execution. | `live_manual`, `guarded_runtime` | Verify off-by-default execution flags. |
| Notebook 11 review packages | Writes interpretive review packages under the Notebook 11 artifact directory. | `artifact_review`, `out_of_ci_scope` | Verify path only; generated files stay out of Git. |
| Caveat register | Records blockers and evidence gaps. | `promotion_readiness_review` | Verify source language only. |
| Archive checkpoint | Optionally checkpoints Notebook 11 state. | `live_manual`, `guarded_runtime` | Confirm false default; do not archive. |

## Manual Candidates

Expanded-run manual-review candidates are source-visible and guarded:

- `buy_and_hold_v1`
- `cross_section_momentum`
- `seeded_random_v1`
- `sma_crossover_v1`

Command success and metric availability for these candidates are raw audit
context only until rerun in a live runtime. Missing split metrics and promotion
gate artifacts remain evidence blockers.

## Non-Claims

Notebook 11 source must not claim alpha, production readiness, strategy
approval, statistical significance, complete platform artifact coverage,
CI/runtime equivalence, archive/checkpoint generality, or promotion-grade
evidence. It should frame results as expanded evidence review,
caveat/blocker review, and promotion-readiness interpretation.

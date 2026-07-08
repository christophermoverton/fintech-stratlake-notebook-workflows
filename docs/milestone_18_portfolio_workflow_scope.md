# Milestone 18 Portfolio Workflow Notebook Scope

## Purpose

This document defines the Milestone 18 scope and implementation plan for
Notebook 15. It addresses Issue #150 and frames the milestone as a distinct
portfolio workflow notebook, not as a continuation of the removed M17
runtime-convention work.

Milestone 18 should add a reviewer-facing portfolio workflow and case-study
notebook that walks through the Fintech + StratLake notebook chain as a
source-safe, narrative-first artifact. The notebook should demonstrate how the
repository orchestrates upstream data ingestion, archive/restore workflows,
feature generation, native strategy research, campaign execution, evidence
review, and governance observation while preserving upstream ownership and
conservative claim boundaries.

## Recommended Milestone Title

```text
M18 - Portfolio Workflow Review and Case Study Notebook
```

## Branch

```text
features/m18-portfolio-workflow-notebook
```

## Target Notebook

| Property | Value |
|---|---|
| Repository path | `notebooks/15_portfolio_workflow_review_and_case_study.ipynb` |
| Notebook title | `Notebook 15 - Portfolio Workflow Review and Case Study` |
| Committed posture | Source-safe, output-free, execution-count-null, preview-oriented |
| Primary upstream apps | `fintech-market-ingestion`; `stratlake-trade-engine` |
| Final stance | `notebook_15_portfolio_workflow_source_safe_review_ready` |

## Milestone Description

Milestone 18 should produce a practical portfolio artifact that helps a reviewer
understand the complete workflow represented by Notebook 00 through Notebook
14. Notebook 15 should be useful without live execution, but it may include
optional, explicitly gated runtime profiles for a prepared Colab or equivalent
notebook environment.

The notebook should not merely summarize prior notebooks. It should implement a
bounded portfolio-oriented walkthrough that reuses repository precedents for
package installation, Colab/Drive setup, Fintech session initialization,
Fintech market-data ingestion or archive restore, StratLake session
initialization, StratLake feature generation or archive restore, native
strategy execution, native strategy comparison, native campaign/portfolio
execution surfaces, artifact review, and source-safe validation.

Notebook 15 should preserve the repository pattern that active runtime work
belongs under `/content`, Google Drive is used only for persistence, backup,
archive, and restore workflows, and generated data, archive packs, restored
files, runtime outputs, logs, IDs, local paths, Drive paths, credentials, and
notebook outputs stay out of Git.

## Portfolio Workflow Thesis

Notebook 15 should present the repository as a portfolio-grade workflow
orchestration layer: Fintech ingests or restores market data, StratLake consumes
the curated handoff to generate or restore features, native StratLake strategy
and campaign commands create research artifacts, and downstream review
surfaces inspect those artifacts with explicit evidence and non-claim
boundaries.

The notebook demonstrates system design, reproducible handoff thinking, and
source-safe notebook workflow construction. It does not demonstrate investment
quality, alpha, strategy approval, statistical significance, promotion
readiness, governance readiness, production readiness, deployment readiness, or
live-trading suitability.

## Target Reviewer Audiences

| Audience | What Notebook 15 should help them see |
|---|---|
| Hiring manager | A concise portfolio story showing data-platform orchestration, practical workflow design, and careful claim boundaries. |
| Technical reviewer | Native-command-first integration across ingestion, archive/restore, feature generation, strategy execution, campaign execution, artifact review, and validation guardrails. |
| Collaborator | Where to enter the notebook sequence, which prior notebooks own detailed evidence, and how to extend the workflow without reimplementing upstream app logic. |
| Future maintainer | The intended Notebook 15 source-safe posture, runtime profile model, follow-up issue map, and validation/non-goal boundaries. |

## Proposed Notebook Section Outline

1. Header, purpose, repository role, expected runtime, upstream apps, and commit
   safety statement.
2. Portfolio case-study thesis and reviewer reading paths.
3. Source-safe runtime profile selector and commented override examples.
4. Package installation and import setup following prior guarded install
   patterns.
5. Colab/local detection, Google Drive guard, and placeholder-only persistence
   configuration.
6. Fintech workspace/session initialization or preview.
7. Fintech market-data workflow: optional live ingestion or archive restore.
8. Fintech data inspection and handoff root validation.
9. StratLake workspace/session initialization.
10. StratLake feature workflow: optional feature generation or feature archive
    restore.
11. Feature-root validation and Fintech-to-StratLake handoff review.
12. Native strategy selection for at least two supported strategies.
13. Native strategy execution or strategy artifact restoration.
14. Bounded strategy output summary and caveat register.
15. Portfolio/campaign case-study configuration using native or documented
    command surfaces.
16. Native portfolio/campaign execution or artifact restoration, gated and
    non-mutating by default.
17. Bounded portfolio artifact review and display-only summaries.
18. Archive backup/checkpoint and archive restore templates for Fintech,
    StratLake, strategy, campaign/portfolio, and handoff state.
19. Evidence-boundary table distinguishing source, runtime observations,
    canonical upstream artifacts, derived review packs, governance
    observations, and portfolio claims.
20. Notebook 00-14 workflow map and links to detailed audit/source-of-record
    documents.
21. Final portfolio review summary, non-goals, validation checklist, and handoff
    to M18.5/M18.6 documentation.

## Runtime Profile Model

Notebook 15 should use a committed default that is preview-only and
non-mutating. Runtime override examples should be commented or disabled in
committed source.

| Profile | Role | Sequential relationship | Source-safe default |
|---|---|---|---|
| `portfolio_preview` | Reviewer walkthrough with no install, Drive mount, restore, ingestion, feature generation, strategy run, portfolio run, checkpoint, or writes. | Baseline committed profile. | Yes; sole committed default. |
| `fintech_market_data_ingestion_run` | Optional live Fintech market-data ingestion using placeholder symbols, dates, and roots after explicit enablement. | Mutually exclusive with Fintech archive restore for the same handoff state. | No. |
| `fintech_market_data_archive_restore` | Optional restore of prior Fintech market-data/session state from a reviewed archive pack. | Alternative to fresh ingestion before StratLake handoff. | No. |
| `stratlake_feature_generation_run` | Optional StratLake feature generation from the reviewed Fintech handoff root. | Runs after Fintech ingestion or restore. Mutually exclusive with feature archive restore for the same feature state. | No. |
| `stratlake_feature_archive_restore` | Optional restore of prior StratLake feature/session state. | Alternative to fresh feature generation before strategy execution. | No. |
| `strategy_execution_run` | Optional native execution of selected strategies using generated or restored features. | Runs after feature generation or restore. | No. |
| `strategy_artifact_restore_review` | Optional loading/review of prior strategy artifacts from restored state. | Alternative to fresh strategy execution. | No. |
| `portfolio_execution_run` | Optional native portfolio or campaign execution associated with selected strategies. | Runs after strategy execution or artifact restore and explicit input review. | No. |
| `workflow_archive_checkpoint` | Optional archive backup/checkpoint of selected workflow state. | Runs only after generated runtime state exists and is reviewed. | No. |
| `workflow_archive_restore` | Optional restore of prior workflow state for review or continuation. | Separate from fresh execution; should not silently blend with generation profiles. | No. |

The notebook should make fresh-generation and archive-restore paths visibly
exclusive for Fintech data and StratLake features. It should also separate
strategy execution from prior-artifact review and keep portfolio/campaign
execution behind explicit operator gates.

## Expected Native Command Surfaces To Reuse

Notebook 15 should reuse existing command examples and classification docs
before introducing any new command shape. The expected command surfaces are:

| Workflow area | Existing precedent to reuse |
|---|---|
| Package installation | Guarded notebook install cells from Notebook 08 through Notebook 14, including existing `fintech-market-ingestion` and `stratlake-trade-engine` package source assumptions. |
| Fintech initialization | `fintech-init-project` patterns from Notebook 01, Notebook 02, Notebook 05, Notebook 06, Notebook 07, Notebook 08, and Notebook 09. |
| Fintech ingestion | `fintech-backfill-daily` patterns from Notebook 01, Notebook 05, and Notebook 06. |
| Fintech backup/restore | `fintech-backup-data pack`, `validate`, `inspect`, and `restore` patterns from Notebook 02 and Notebook 03, with Notebook 05/06 preview guidance. |
| StratLake initialization | `stratlake-init-session` patterns from Notebook 04 through Notebook 09, and `stratlake-init-notebook --root /content/stratlake` where Notebook 13/14 establish that surface. |
| StratLake feature generation | `stratlake-build-features` patterns from Notebook 05 and Notebook 06. |
| StratLake archive backup/restore | `stratlake-session-export`, `stratlake-session-archive-bootstrap`, and `stratlake-session-archive-restore-bootstrap` patterns from Notebook 05 through Notebook 14. |
| Strategy execution | `stratlake-run-strategy` patterns from Notebook 07 through Notebook 11. |
| Strategy comparison | Native strategy comparison loop and bounded stdout parsing from Notebook 09. |
| Campaign or portfolio execution | `stratlake-run-research-campaign --config <config>` and generated execution-candidate guardrails from Notebook 13; any portfolio-specific surface should be documented before use and must remain native-owned. |
| Evidence review and governance observation | `stratlake-build-evidence-review`, native strict validation, `stratlake-run-promotion-governance-report`, and catalog/lineage observation boundaries from Notebook 14. |

If a portfolio-specific native command is not already documented in this
repository, M18.2/M18.3 should prefer a documented campaign/portfolio command
surface from `stratlake-trade-engine` or record the gap as a conservative
follow-up. Notebook 15 must not implement a notebook-owned portfolio engine.

## Source-Safe Acceptance Criteria

- The milestone branch is recorded as
  `features/m18-portfolio-workflow-notebook`.
- The notebook path is recorded as
  `notebooks/15_portfolio_workflow_review_and_case_study.ipynb`.
- The notebook title is recorded as
  `Notebook 15 - Portfolio Workflow Review and Case Study`.
- The milestone is framed as a distinct portfolio workflow notebook, not a
  continuation of removed M17 runtime-convention work.
- The notebook defaults to `portfolio_preview` or an equivalent preview-only
  profile.
- Runtime override examples are commented, placeholder-driven, and disabled by
  default.
- The source contains no committed credentials, tokens, Drive paths, local user
  paths, runtime IDs, run IDs, review IDs, archive IDs, generated inventories,
  logs, generated data, archive packs, restored files, runtime artifacts,
  execution outputs, or execution counts.
- Fresh Fintech ingestion and Fintech archive restore are clearly mutually
  exclusive choices for a given market-data handoff.
- Fresh StratLake feature generation and StratLake feature archive restore are
  clearly mutually exclusive choices for a given feature handoff.
- Strategy execution uses native StratLake strategy surfaces and selects at
  least two supported strategies through configuration.
- Portfolio/campaign execution uses documented/native surfaces and does not
  reimplement portfolio logic in notebook code.
- Artifact review remains bounded, display-only, and non-authoritative.
- The notebook distinguishes committed source-safe behavior from optional
  runtime observations.
- The notebook preserves upstream ownership by `fintech-market-ingestion` and
  `stratlake-trade-engine`.
- Source-only validation is added in later M18 issues before merge readiness is
  claimed.

## Non-Claim Boundaries

Notebook 15 and M18 documentation must not claim:

- investment recommendation;
- strategy approval;
- positive alpha;
- statistical significance;
- promotion readiness;
- governance readiness;
- deployment readiness;
- production readiness;
- live-trading suitability;
- source/runtime equivalence;
- portfolio performance quality;
- authoritative performance reporting;
- native artifact completeness unless separately verified by native tools and
  documented as runtime-only evidence.

## Non-Goals

- Do not create a performance report or investment recommendation.
- Do not execute live ingestion, restore, campaign execution, evidence-review
  build, governance reporting, archive checkpointing, or Drive mounting in
  repository validation.
- Do not reimplement Fintech market-data ingestion, backup/restore, or session
  logic.
- Do not reimplement StratLake feature generation, strategy, backtest,
  campaign, portfolio, artifact, validation, promotion, or governance logic.
- Do not replace existing detailed notebook import audits or smoke-audit
  summaries.
- Do not commit generated data, archive packs, restore outputs, strategy
  artifacts, campaign/portfolio artifacts, governance reports, plots, logs, or
  runtime summaries.
- Do not treat derived review packs as canonical governance evidence.

## Follow-Up Issue Mapping

| Issue | Scope |
|---|---|
| #151 / M18.2 | Stage the source-safe Notebook 15 file with clean title/header, source-safe sections, output-free cells, null execution counts, and preview defaults. |
| #152 / M18.3 | Add the portfolio narrative, workflow map, reviewer reading paths, evidence-boundary table, and conservative Notebook 13 to Notebook 14 case-study framing. |
| #153 / M18.4 | Add source-only validation for Notebook 15 hygiene, required sections, source-safe defaults, and non-claim boundaries. |
| #154 / M18.5 | Update README, notebook index, and Notebook 15 portfolio/import audit documentation links. |
| #155 / M18.6 | Add Milestone 18 merge-readiness closeout with validation results, changed files, PR title/description, and final source-safe stance. |

## Completion Stance For Issue #150

```text
notebook_15_portfolio_workflow_source_safe_review_ready
```

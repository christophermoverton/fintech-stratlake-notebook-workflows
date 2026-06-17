# Milestone 16 Merge Readiness - Notebook 13 Native Campaign Execution Import

## Summary

Milestone 16 imports Notebook 13 as the source-safe native campaign execution
and artifact generation successor to Notebook 12.

This document is the final Notebook 13 source-safe import audit and PR-readiness
record after optional M16.7 runtime smoke evidence was recorded outside Git.

Committed notebook:

- `notebooks/13_stratlake_native_campaign_execution_and_artifact_generation.ipynb`

Notebook identity:

- Title: Notebook 13 - StratLake Native Campaign Execution and Artifact
  Generation.
- Milestone: M16 - Notebook 13 Native Campaign Execution and Artifact
  Generation Import.
- Role: source-safe, guarded native campaign execution and artifact generation
  workflow.

Notebook 13 extends Notebook 12 from campaign evidence review into guarded
native StratLake campaign execution. It composes native StratLake command
surfaces for workspace initialization, archive restore, generated execution
candidate config review, native command preflight, optional native campaign
execution, artifact inventory, caveat registration, and handoff. It does not
replace native StratLake orchestration, reporting, governance, promotion, or
artifact semantics.

Final stance:

```text
notebook_13_import_pr_ready_source_safe_native_smoke_audited
```

Notebook 13 does not claim production readiness, strategy approval, promotion
readiness, governance readiness, statistical significance, alpha validation,
split-metric completeness, artifact completeness, generated configs as upstream
native templates, committed runtime smoke evidence, source/runtime equivalence,
or CI proof of live native runtime behavior.

## Branch And Issue Sequence

| Issue | Branch | Stance |
|---|---|---|
| #126 / M16.1 | `features/m16-1-stage-clean-notebook-13-native-campaign-execution` | `notebook_13_staged_cleaned_source_safe` |
| #127 / M16.2 | `features/m16-2-classify-notebook-13-runtime-native-execution-surfaces` | `notebook_13_runtime_surfaces_classified_source_safe` |
| #128 / M16.3 | `features/m16-3-add-notebook-13-static-source-tests` | `notebook_13_source_static_contracts_covered` |
| #129 / M16.4 | `features/m16-4-add-notebook-13-native-execution-guardrails` | `notebook_13_native_execution_guardrails_ready` |
| #130 / M16.5 | `features/m16-5-add-notebook-13-import-documentation-smoke-audit` | `notebook_13_import_docs_and_smoke_audit_ready` |
| #132 / M16.7 | `features/m16-7-run-notebook-13-runtime-smoke-checks` | `notebook_13_runtime_smoke_verified_without_committed_outputs` |
| #131 / M16.6 | `features/m16-6-final-notebook-13-pr-readiness` | `notebook_13_import_pr_ready_source_safe_native_smoke_audited` |

## Files In Scope

Notebook source:

- `notebooks/13_stratlake_native_campaign_execution_and_artifact_generation.ipynb`

Documentation:

- `docs/notebook_13_command_surface_classification.md`
- `docs/notebook_13_import_audit.md`
- `docs/notebook_13_smoke_audit_summary.md`
- `docs/milestone_16_merge_readiness.md`
- `docs/notebook_index.md`
- `README.md`

Tests:

- `tests/test_notebook_13_source_contracts.py`
- `tests/test_notebook_13_execution_guardrails.py`
- `tests/test_notebook_13_artifact_handoff_contracts.py`

## Source-Safe Import State

The committed Notebook 13 source remains:

- Present at
  `notebooks/13_stratlake_native_campaign_execution_and_artifact_generation.ipynb`.
- Valid notebook JSON.
- 45 cells total.
- 26 markdown cells.
- 19 code cells.
- Output-free.
- Execution-count-null.
- Defaulted to `campaign_execution_preview`.
- Guarded against archive restore by default.
- Guarded against generated config execution by default.
- Guarded against native campaign execution by default.
- Guarded against optional governance/reporting command execution by default.
- Guarded against archive checkpointing by default.
- Free of committed generated runtime configs.
- Free of committed native campaign artifacts.
- Free of committed restored archive material, Google Drive material, Colab
  outputs, credentials, secrets, private paths, and executed notebook artifacts.

The committed notebook is not an executed runtime smoke artifact.

Generated runtime outputs belong outside Git under runtime artifact roots such
as:

```text
artifacts/notebook_13_native_campaign_execution_and_artifact_generation/
```

The existing untracked `.claude/` directory remains outside this milestone
scope and is not staged.

## Runtime Profiles And Gates

Notebook 13 preserves these profiles:

- `campaign_execution_preview` - committed source-safe default.
- `campaign_execution_preflight` - manual restore and input-readiness preflight.
- `campaign_execution_run` - manual native execution profile.
- `campaign_execution_run_with_archive_checkpoint` - manual native execution
  plus checkpoint profile.

Runtime gates remain explicit:

- `RUN_STRATLAKE_SESSION_INIT`
- `RUN_ARCHIVE_RESTORE`
- `NOTEBOOK13_ALLOW_ARCHIVE_RESTORE`
- `NOTEBOOK13_CREATE_EXECUTION_CONFIGS`
- `NOTEBOOK13_MARK_INPUTS_USER_REVIEWED`
- `NOTEBOOK13_ALLOW_NOTEBOOK_GENERATED_CONFIG_EXECUTION`
- `RUN_NATIVE_CAMPAIGN_EXECUTION`
- `NOTEBOOK13_ALLOW_NATIVE_EXECUTION`
- `RUN_OPTIONAL_REPORT_COMMANDS`
- `RUN_OPTIONAL_GOVERNANCE_COMMANDS`
- `RUN_ARCHIVE_CHECKPOINT`
- `NOTEBOOK13_ALLOW_ARCHIVE_CHECKPOINT`

Restore and native execution command surfaces remain:

```text
stratlake-session-archive-restore-bootstrap \
  --archive-root <Google Drive/session archive root>/<archive-id> \
  --target-root /content/stratlake \
  --validate-before-restore \
  --inspect-before-restore \
  --overwrite-policy overwrite_allowed

stratlake-run-research-campaign --config <config>
```

Repository validation remains source-only. It does not execute Notebook 13
cells, install packages, mount Drive, restore archives, initialize live
sessions, generate runtime configs, run native campaigns, run governance or
reporting commands, checkpoint archives, or write runtime artifacts.

## Generated Config And Catalog Guardrails

Generated campaign and universe configs remain:

- notebook-generated;
- execution candidates;
- `native_template: false`;
- review-required;
- not canonical upstream StratLake templates.

Execution of notebook-generated configs requires reviewed runtime inputs, the
generated-config allow gate, successful preflight, and the native execution
allow gate for actual execution.

Catalog and strategy guardrails remain intact:

- Restored catalog paths are runtime inputs, not source artifacts.
- Strategy catalog: `/content/stratlake/configs/strategies.yml`.
- Portfolio catalog: `/content/stratlake/configs/portfolios.yml`.
- Alpha catalog: `/content/stratlake/configs/alphas.yml`.
- Strategy aliases/defaults are visible in status and handoff summaries.
- Unknown requested strategies block execution.
- Missing required catalogs block the relevant execution path.
- Requested alpha targets require a real alpha catalog.
- Empty alpha catalog fallback is strategy-only and is not alpha readiness,
  alpha validation, or promotion evidence.

## Runtime Smoke Evidence

Issue #132 / M16.7 recorded optional manual runtime smoke evidence across three
profiles:

| Profile | Evidence stance |
|---|---|
| `campaign_execution_preview` | Verified source-safe defaults and no archive restore or native execution. |
| `campaign_execution_preflight` | Verified StratLake init, archive restore return code 0, preflight success, native input readiness, and no native execution. |
| `campaign_execution_run` | Verified archive restore return code 0, preflight success, `stratlake-run-research-campaign` return code 0, empty execution blockers, and native artifacts detected. |

The executed notebook artifacts contained outputs and execution counts and
remain outside Git. The smoke evidence is manual runtime evidence only. It is
not committed notebook output, not source-only validation evidence, and not CI
evidence.

Native execution success is tied to `campaign_execution_returncode=0`. Artifact
discovery alone is not treated as proof of current-session execution.
Governance rows were 0, so no governance readiness claim is made. Split metric
rows were 0, so no split-metric completeness claim is made. Artifact
completeness is not claimed.

## Static And Source-Only Coverage

Issue #128 added Notebook 13 static/source-only tests. Issue #129 strengthened
them around generated config provenance, catalog readiness, strategy
resolution, alpha fallback, execution blockers, caveat preservation, artifact
handoff, and non-claim boundaries.

Focused Notebook 13 source-only results:

```text
python -m pytest tests/test_notebook_13_source_contracts.py -q -> 20 passed
python -m pytest tests/test_notebook_13_execution_guardrails.py -q -> 20 passed
python -m pytest tests/test_notebook_13_artifact_handoff_contracts.py -q -> 19 passed
```

These tests parse committed source files only. They do not execute notebook
cells, import live StratLake runtime packages as a requirement, call native CLI
commands, mount Google Drive, restore archives, generate campaign configs, write
runtime artifacts, depend on Colab, depend on network access, or depend on
secrets.

## Validation Result

Final M16.6 validation commands:

```bash
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
python scripts/scan_for_secret_patterns.py .
python -m pytest tests/test_notebook_13_source_contracts.py -q
python -m pytest tests/test_notebook_13_execution_guardrails.py -q
python -m pytest tests/test_notebook_13_artifact_handoff_contracts.py -q
pytest
```

Final M16.6 validation result:

```text
check_notebooks_no_outputs.py notebooks -> passed; checked 14 notebook(s)
validate_repo_cleanliness.py . -> passed
scan_for_secret_patterns.py . -> passed
python -m pytest tests/test_notebook_13_source_contracts.py -q -> 20 passed
python -m pytest tests/test_notebook_13_execution_guardrails.py -q -> 20 passed
python -m pytest tests/test_notebook_13_artifact_handoff_contracts.py -q -> 19 passed
pytest -> 961 passed, 5 warnings
```

The warnings are existing repository warnings and are not new Notebook 13 source
artifacts.

## PR Summary

This PR completes Milestone 16 by importing Notebook 13 - StratLake Native
Campaign Execution and Artifact Generation - as a cleaned, source-safe, guarded
native campaign execution notebook.

Key changes:

- Added Notebook 13 at
  `notebooks/13_stratlake_native_campaign_execution_and_artifact_generation.ipynb`.
- Added Notebook 13 command/runtime surface classification.
- Added Notebook 13 source-only static tests.
- Strengthened generated config, catalog, strategy, alpha, native execution,
  artifact, caveat, and handoff guardrails.
- Added import audit and smoke audit documentation.
- Recorded optional M16.7 manual runtime smoke evidence outside Git across
  preview, preflight, and run profiles.
- Updated README and notebook index references.
- Added this final M16 merge-readiness handoff.

Completion stance:

```text
notebook_13_import_pr_ready_source_safe_native_smoke_audited
```

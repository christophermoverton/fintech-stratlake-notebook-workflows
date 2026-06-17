# Notebook 13 Smoke Audit Summary

## Purpose

This document summarizes the Notebook 13 smoke-audit posture after Issues #126
through #130. It records source-safe validation, manual runtime smoke context,
guardrails, caveats, and remaining claim boundaries for:

```text
notebooks/13_stratlake_native_campaign_execution_and_artifact_generation.ipynb
```

Notebook 13 extends Notebook 12 from campaign evidence review into guarded
native campaign execution and artifact generation. It remains a source-safe
notebook import in Git and a manual/runtime workflow when explicit gates are
enabled.

## Source-Only Audit

Source-only audit is complete for the committed notebook:

- Outputs are cleared.
- Execution counts are `null`.
- Default profile is `campaign_execution_preview`.
- Archive restore is disabled by default.
- Native campaign execution is disabled by default.
- Generated configs are execution candidates, not upstream native templates.
- Runtime artifacts and restored session material are excluded from Git.
- Static/source-only tests cover profiles, gates, generated config provenance,
  catalog/strategy/alpha guardrails, artifact boundaries, handoff fields, and
  non-claim language.

This source-only audit does not execute notebook cells, install packages, mount
Drive, restore archives, initialize sessions, run native StratLake commands,
write artifacts, or prove live Colab/manual runtime behavior.

## Runtime Profile Posture

| Surface | Current audit posture | Boundary |
|---|---|---|
| `campaign_execution_preview` | Committed default | Source-safe preview; no archive restore or native execution by default |
| `campaign_execution_preflight` | Manual/runtime profile | May restore and preflight only when gates are enabled |
| `campaign_execution_run` | Manual/runtime profile | Requires reviewed inputs, generated-config allow gates when relevant, successful preflight, and `NOTEBOOK13_ALLOW_NATIVE_EXECUTION=true` |
| `campaign_execution_run_with_archive_checkpoint` | Manual/runtime profile | Adds archive checkpointing only when execution succeeds and `NOTEBOOK13_ALLOW_ARCHIVE_CHECKPOINT=true` |
| Archive restore | Manual/runtime | Uses Google Drive/session archive root and local `/content/stratlake`; not part of source validation |
| Native campaign execution | Manual/runtime | Uses `stratlake-run-research-campaign --config <config>`; success requires return code 0 |
| Optional governance/reporting | Manual/runtime | May be discovered or run only when enabled; missing governance remains a caveat |
| Artifact discovery | Runtime review surface | Does not prove current-session native execution |

## Manual Native Smoke Context

The development companion records a manual runtime smoke where:

- `stratlake-run-research-campaign` returned code 0.
- Native campaign artifacts were detected.
- Archive restore had succeeded in the runtime context.
- Handoff status was recorded as a Notebook 13 native campaign execution smoke
  pass in the executed runtime artifact.

This smoke context is intentionally conservative:

- The executed notebook artifact is not committed.
- Runtime outputs are not committed.
- Generated configs are not committed as source artifacts.
- Native campaign artifacts are not committed.
- Restored archives and Google Drive material are not committed.
- The smoke is not CI evidence.
- The smoke is not production, promotion, governance, alpha, or statistical
  evidence.

## Guardrails Preserved

Generated config guardrails:

- Generated campaign config source:
  `notebook13_generated_execution_candidate_config`.
- Generated universe config source:
  `notebook13_generated_execution_candidate_universe`.
- Generated configs are `notebook-generated`, `execution-candidate`, and
  `native_template: false`.
- Generated config execution requires user review and
  `NOTEBOOK13_ALLOW_NOTEBOOK_GENERATED_CONFIG_EXECUTION=true`.

Catalog and strategy guardrails:

- Strategy catalog:
  `/content/stratlake/configs/strategies.yml`.
- Portfolio catalog:
  `/content/stratlake/configs/portfolios.yml`.
- Alpha catalog:
  `/content/stratlake/configs/alphas.yml`.
- Strategy aliases/defaults are recorded.
- Unknown requested strategies block native execution.
- Requested alpha targets require a real alpha catalog.
- Empty alpha catalog fallback is strategy-only and notebook-local.

Execution guardrails:

- Native execution cannot run in `campaign_execution_preview`.
- Native execution cannot run merely because artifacts are discovered.
- Native execution requires a run profile and `NOTEBOOK13_ALLOW_NATIVE_EXECUTION`.
- Preflight must succeed.
- Campaign config, universe config, and feature inputs must be ready/reviewed.
- Catalog, strategy, and alpha blockers must be absent.
- Success is claimed only when the native return code is 0.

## Artifact And Handoff Boundaries

Notebook 13 distinguishes:

- native campaign artifacts;
- notebook summary artifacts;
- generated execution-candidate configs;
- restored session inputs;
- candidate campaign context;
- caveat register;
- execution summary;
- handoff summary.

Handoff summaries preserve execution requested/enabled/status/succeeded fields,
execution blockers, catalog/strategy/alpha blockers, caveats, and explicit
non-claim flags. They are runtime review artifacts and remain outside Git.

## Validation Summary

Latest local validation recorded in M16.4:

```text
python scripts/check_notebooks_no_outputs.py notebooks -> passed; checked 14 notebook(s)
python scripts/validate_repo_cleanliness.py . -> passed
python scripts/scan_for_secret_patterns.py . -> passed
python -m pytest tests/test_notebook_13_source_contracts.py -q -> 20 passed
python -m pytest tests/test_notebook_13_execution_guardrails.py -q -> 20 passed
python -m pytest tests/test_notebook_13_artifact_handoff_contracts.py -q -> 19 passed
pytest -> 961 passed, 5 warnings
```

This is local validation evidence. It does not replace live Colab/manual
runtime validation or remote CI evidence.

## Non-Claims

This smoke audit does not claim:

- Production readiness.
- Strategy approval.
- Promotion readiness.
- Governance readiness without native governance evidence.
- Statistical significance.
- Alpha validation.
- Generated configs are upstream native templates.
- Runtime smoke evidence is committed notebook output.
- Source-only validation is equivalent to live Colab/manual runtime validation.

## Remaining Manual Runtime Next Actions

Remaining manual/runtime actions, when desired:

- Rerun a guarded manual runtime smoke from source-safe `campaign_execution_preview`.
- Restore reviewed session material into `/content/stratlake`.
- Provide or review native/user-supplied campaign, universe, feature, strategy,
  portfolio, and alpha catalog inputs.
- Run `campaign_execution_preflight` before any native execution.
- Run `campaign_execution_run` only after all review and allow gates are set.
- Run optional governance/reporting only after native artifacts exist.
- Keep all generated runtime artifacts outside Git.

Completion stance:

```text
notebook_13_import_docs_and_smoke_audit_ready
```

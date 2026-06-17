# Notebook 13 Smoke Audit Summary

## Purpose

This document summarizes the Notebook 13 smoke-audit posture after Issues #126
through #130 and the optional M16.7 runtime smoke verification. It records
source-safe validation, manual runtime smoke context,
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

## M16.7 Optional Runtime Smoke Verification

Issue #132 / M16.7 records optional manual runtime smoke verification across
three audited profiles. The executed notebook artifacts contained outputs and
execution counts and are valid smoke evidence, but they remain outside Git and
are not committed source.

Combined M16.7 stance:

```text
notebook_13_runtime_smoke_verified_without_committed_outputs
```

### Profile Results

| Profile | Evidence type | Key observed result | Stance |
|---|---|---|---|
| `campaign_execution_preview` | Source-safe preview evidence | Verified source-safe defaults, archive restore not requested, native execution not requested, checkpoint not requested, and one expected preflight blocker for missing native strategy config in preview context. | `notebook_13_preview_profile_verified_source_safe_no_native_execution` |
| `campaign_execution_preflight` | Review-gated preflight evidence | Verified StratLake init succeeded, archive restore returned code 0, preflight succeeded, runtime inputs were ready, and native execution remained not requested. | `notebook_13_preflight_profile_verified_restore_and_input_readiness_no_native_execution` |
| `campaign_execution_run` | Full native runtime smoke evidence | Verified archive restore returned code 0, native preflight succeeded, `stratlake-run-research-campaign` returned code 0, execution blockers were empty, and native campaign artifacts were detected. | `notebook_13_native_campaign_execution_smoke_passed_with_artifacts` |

### Preview Profile Evidence

The preview run used `NOTEBOOK13_TEST_PROFILE=campaign_execution_preview`.

Observed source-safe controls:

- `default_profile_is_source_safe=True`.
- `allow_native_execution=False`.
- `allow_archive_restore=False`.
- `allow_archive_checkpoint=False`.
- `allow_notebook_generated_config_execution=False`.
- `mark_inputs_user_reviewed=False`.

Observed non-execution state:

- `archive_restore_requested=False`.
- `archive_restore_enabled=False`.
- `archive_restore_status=not_requested`.
- `campaign_execution_requested=False`.
- `campaign_execution_enabled=False`.
- `campaign_execution_returncode=None`.
- `campaign_execution_succeeded=False`.
- `campaign_execution_claim_made=False`.
- `campaign_execution_status=not_requested`.
- `archive_checkpoint_requested=False`.
- `archive_checkpoint_enabled=False`.
- `archive_status=not_requested`.

Observed preview preflight state:

- `campaign_command_shape_preflight_succeeded=True`.
- `campaign_runtime_input_preflight_succeeded=True`.
- `native_execution_input_ready=False`.
- `campaign_preflight_succeeded=False`.
- `preflight_hard_blocker_count=1`.
- Blocker: native strategy config path unavailable for generated campaign
  config.

Preview evidence verifies the committed source-safe/non-executing posture. It is
not native campaign execution evidence.

### Preflight Profile Evidence

The preflight run used `NOTEBOOK13_TEST_PROFILE=campaign_execution_preflight`.

Observed review gates:

- `allow_native_execution=False`.
- `allow_archive_restore=True`.
- `allow_archive_checkpoint=False`.
- `allow_notebook_generated_config_execution=True`.
- `mark_inputs_user_reviewed=True`.

Observed restore and readiness state:

- `selected_stratlake_init_succeeded=True`.
- `archive_restore_requested=True`.
- `archive_restore_enabled=True`.
- `archive_restore_returncode=0`.
- `archive_restore_succeeded=True`.
- `archive_restore_status=succeeded`.
- `restore_archive_id=notebook-session-001`.
- `restore_target_root=/content/stratlake`.
- `campaign_preflight_requested=True`.
- `campaign_preflight_succeeded=True`.
- `campaign_command_shape_preflight_succeeded=True`.
- `campaign_runtime_input_preflight_succeeded=True`.
- `native_execution_input_ready=True`.
- `primary_campaign_command_available=True`.
- `preflight_hard_blocker_count=0`.
- `preflight_hard_blockers=[]`.

Observed native execution state:

- `campaign_execution_requested=False`.
- `campaign_execution_enabled=False`.
- `campaign_execution_returncode=None`.
- `campaign_execution_succeeded=False`.
- `campaign_execution_claim_made=False`.
- `campaign_execution_status=not_requested`.

Observed artifact inventory context:

- `campaign_artifact_rows=13`.
- `native_campaign_artifact_rows=0`.
- `candidate_campaign_context_rows=6`.
- `report_rows=2`.
- `governance_rows=0`.
- `log_rows=2`.

Preflight evidence verifies restore and runtime input readiness without native
campaign execution.

### Full Native Run Profile Evidence

The run used `NOTEBOOK13_TEST_PROFILE=campaign_execution_run`.

Observed review gates:

- `allow_native_execution=True`.
- `allow_archive_restore=True`.
- `allow_archive_checkpoint=False`.
- `allow_notebook_generated_config_execution=True`.
- `mark_inputs_user_reviewed=True`.

Observed restore and preflight state:

- `archive_restore_requested=True`.
- `archive_restore_enabled=True`.
- `archive_restore_returncode=0`.
- `archive_restore_succeeded=True`.
- `archive_restore_status=succeeded`.
- `restore_archive_id=notebook-session-001`.
- `restore_target_root=/content/stratlake`.
- `restore_overwrite_policy=overwrite_allowed`.
- `archive_restore_runtime_seconds=2.505193`.
- `campaign_preflight_requested=True`.
- `campaign_preflight_succeeded=True`.
- `campaign_command_shape_preflight_succeeded=True`.
- `campaign_runtime_input_preflight_succeeded=True`.
- `native_execution_input_ready=True`.
- `primary_campaign_command=stratlake-run-research-campaign`.
- `primary_campaign_command_available=True`.
- `primary_campaign_command_help_checked=True`.
- `preflight_hard_blocker_count=0`.
- `preflight_hard_blockers=[]`.

Observed native execution state:

- `campaign_execution_requested=True`.
- `campaign_execution_enabled=True`.
- `campaign_execution_returncode=0`.
- `campaign_execution_succeeded=True`.
- `campaign_execution_runtime_seconds=6.372137`.
- `campaign_execution_status=succeeded`.
- `execution_blockers=[]`.

Observed artifact inventory context:

- `campaign_artifact_rows=37`.
- `native_campaign_artifact_rows=13`.
- `native_campaign_marker_rows=18`.
- `candidate_campaign_context_rows=18`.
- `campaign_context_loaded=True`.
- `campaign_review_rows=6`.
- `manifest_rows=4`.
- `run_registry_rows=1`.
- `metrics_rows=2`.
- `split_metrics_rows=0`.
- `report_rows=3`.
- `governance_rows=0`.
- `log_rows=3`.

Native execution smoke passed with artifacts detected because
`campaign_execution_returncode=0`. Governance rows were 0, so no governance
readiness claim is made. Split metric rows were 0, so no split-metric
completeness claim is made.

## Manual Native Smoke Context

The development companion and M16.7 audit record manual runtime smoke where:

- `stratlake-run-research-campaign` returned code 0 in the full run profile.
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
- Preview/preflight evidence is not native campaign execution evidence.
- Artifact discovery alone is not proof of current-session execution.
- The smoke is not production, promotion, governance, alpha, or statistical
  evidence.
- The smoke does not prove artifact completeness.

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

Latest local validation recorded in M16.7:

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
- Executed notebook artifacts are committed source.
- Generated runtime configs are committed source artifacts.
- Native campaign artifacts are committed.
- Restored archives or Google Drive material are committed.
- Artifact discovery alone proves current-session execution.
- Split-metric completeness.
- Artifact completeness.
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
notebook_13_runtime_smoke_verified_without_committed_outputs
```

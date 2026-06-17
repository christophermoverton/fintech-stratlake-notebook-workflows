# Notebook 13 Import Audit

## Purpose

This audit records the M16 import of Notebook 13 for Issues #126 through #130
and the optional M16.7 runtime smoke evidence recorded in Issue #132.

- Milestone: M16 - Notebook 13 Native Campaign Execution and Artifact
  Generation Import.
- Notebook title: Notebook 13 - StratLake Native Campaign Execution and
  Artifact Generation.
- Committed path:
  `notebooks/13_stratlake_native_campaign_execution_and_artifact_generation.ipynb`.
- Source role: source-safe native campaign execution and artifact generation
  workflow.
- Current source status: source-safe, output-free, execution-count-null,
  guarded, statically validated, and non-claiming.
- Current stance: `notebook_13_runtime_smoke_verified_without_committed_outputs`.

M16 Notebook 13 issue stances:

- #126: `notebook_13_staged_cleaned_source_safe`.
- #127: `notebook_13_runtime_surfaces_classified_source_safe`.
- #128: `notebook_13_source_static_contracts_covered`.
- #129: `notebook_13_native_execution_guardrails_ready`.
- #130: `notebook_13_import_docs_and_smoke_audit_ready`.
- #132: `notebook_13_runtime_smoke_verified_without_committed_outputs`.

Notebook 13 extends Notebook 12 from campaign evidence gap review into guarded
native StratLake campaign execution and artifact generation. It restores
archived StratLake session material when explicitly enabled, initializes a
notebook workspace, discovers native command surfaces, builds review-gated
execution-candidate configs, preflights native command shape and runtime inputs,
and runs `stratlake-run-research-campaign` only when explicit runtime gates are
enabled.

Notebook 13 composes native StratLake command surfaces. It does not replace
native StratLake campaign orchestration, manifests, run registries, metrics,
split metrics, reporting, governance, promotion decisions, archive restore, or
archive checkpoint behavior.

## Source-Safe Staging Summary

Source facts after M16.4:

- Notebook exists at the committed path.
- Code-cell outputs are cleared.
- Code-cell execution counts are `null`.
- Default profile is `campaign_execution_preview`.
- Archive restore is disabled by default.
- Native campaign execution is disabled by default.
- Optional governance/reporting command execution is disabled by default.
- Archive checkpointing is disabled by default.
- No runtime artifacts are committed.
- No restored archives, Google Drive material, credentials, generated runtime
  configs, native campaign outputs, Colab outputs, or execution artifacts are
  committed.

Generated runtime outputs belong outside Git under runtime artifact roots such
as:

```text
artifacts/notebook_13_native_campaign_execution_and_artifact_generation/
```

Committed source validation may inspect notebook JSON, source text, docs, and
tests. It must not execute Notebook 13 cells, install packages, mount Google
Drive, restore archives, initialize Fintech or StratLake sessions, generate
runtime configs as committed artifacts, run native StratLake campaigns, run
governance/reporting commands, or write runtime artifacts.

## Runtime Profiles And Gates

Notebook 13 preserves these profiles:

| Profile | Source/runtime posture |
|---|---|
| `campaign_execution_preview` | Committed default. Discovers command/config surfaces and performs source-safe preview/preflight with native execution disabled. |
| `campaign_execution_preflight` | Manual profile for workspace/session initialization, archive restore, generated-input review, and command/input preflight. |
| `campaign_execution_run` | Manual full native execution profile. Requires explicit native execution and review gates. |
| `campaign_execution_run_with_archive_checkpoint` | Manual full native execution plus optional archive checkpoint. Requires the archive checkpoint allow gate. |

Runtime gates and profile flags:

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

Native execution requires a run profile, `NOTEBOOK13_ALLOW_NATIVE_EXECUTION`,
successful native command build, successful preflight, reviewed runtime inputs,
generated-config allow gates when generated configs are selected, and no
catalog, strategy, alpha, feature, campaign-config, or universe-config blockers.

## Native Command And Restore Surfaces

Guarded restore command shape:

```text
stratlake-session-archive-restore-bootstrap \
  --archive-root <Google Drive/session archive root>/<archive-id> \
  --target-root /content/stratlake \
  --validate-before-restore \
  --inspect-before-restore \
  --overwrite-policy overwrite_allowed
```

Native execution command shape:

```text
stratlake-run-research-campaign --config <config>
```

Restore and native execution are manual/runtime operations. They are not part of
repository CI/source validation.

## Generated Config And Catalog Guardrails

Generated campaign and universe configs remain:

- notebook-generated;
- execution candidates;
- `native_template: false`;
- review-required;
- gated by `NOTEBOOK13_ALLOW_NOTEBOOK_GENERATED_CONFIG_EXECUTION`;
- not canonical upstream StratLake templates.

Execution of notebook-generated configs requires reviewed runtime inputs,
`NOTEBOOK13_MARK_INPUTS_USER_REVIEWED=true` or equivalent specific review flags,
`NOTEBOOK13_ALLOW_NOTEBOOK_GENERATED_CONFIG_EXECUTION=true`, successful
preflight, and `NOTEBOOK13_ALLOW_NATIVE_EXECUTION=true` for actual native
execution.

Catalog and strategy guardrails:

- Restored catalog paths are runtime inputs, not source artifacts.
- Strategy catalog readiness is explicit for
  `/content/stratlake/configs/strategies.yml`.
- Portfolio catalog readiness is explicit for
  `/content/stratlake/configs/portfolios.yml`.
- Alpha catalog readiness is explicit for
  `/content/stratlake/configs/alphas.yml`.
- Strategy aliases/defaults are visible in preflight and handoff summaries.
- Unknown requested strategies block execution.
- Missing required catalogs block the relevant execution path.
- Requested alpha targets require a real alpha catalog.
- Empty alpha catalog fallback is notebook-local and strategy-only; it is not
  alpha readiness, alpha validation, promotion evidence, or a substitute for a
  real alpha catalog when alpha targets are requested.

## Artifact And Handoff Boundaries

Notebook 13 runtime artifact classes:

- native campaign artifacts;
- notebook summary artifacts;
- generated execution-candidate configs;
- restored session inputs;
- candidate campaign context;
- caveat register;
- execution summary;
- handoff summary.

Artifact discovery does not prove current-session native execution. The
execution summary records whether execution was requested, enabled, blocked,
succeeded, failed, or skipped. Current-session execution success may be claimed
only when `stratlake-run-research-campaign` returns code 0.

Handoff summaries preserve blockers, caveats, status fields, runtime input
readiness, catalog/strategy/alpha readiness, and explicit non-claim flags.

## Native Smoke Audit Summary

The development companion records an optional manual runtime smoke where
`stratlake-run-research-campaign` returned code 0 and native campaign artifacts
were detected. That smoke evidence is manual/runtime context only:

- It is not committed notebook output.
- It is not source-only validation evidence.
- It is not CI evidence.
- It does not prove artifact completeness.
- It does not prove production readiness.
- It does not prove strategy approval.
- It does not prove alpha validation.
- It does not prove statistical significance.
- It does not prove governance or promotion readiness.

The committed notebook was restored to `campaign_execution_preview` before
import and remains output-free and execution-count-null.

## M16.7 Evidence Addendum

Issue #132 / M16.7 directly audited optional manual runtime smoke across three
profiles:

- `campaign_execution_preview`
- `campaign_execution_preflight`
- `campaign_execution_run`

The preview profile verified source-safe defaults: archive restore was not
requested, native execution was not requested, checkpointing was not requested,
and the expected preview blocker was recorded for unavailable native strategy
config in the preview context.

The preflight profile verified gated restore and input readiness without native
execution: StratLake init succeeded, archive restore returned code 0, preflight
succeeded, native execution input readiness was true, and
`campaign_execution_status=not_requested`.

The run profile verified full native runtime smoke: archive restore returned
code 0, native preflight succeeded, `stratlake-run-research-campaign` returned
code 0, execution blockers were empty, native campaign artifacts were detected,
and the handoff status was
`notebook_13_native_campaign_execution_smoke_passed_with_artifacts`.

These executed notebook artifacts remain outside Git. They are manual runtime
evidence only and are not committed notebook output, source-only validation
evidence, or CI evidence. Generated runtime configs, native campaign artifacts,
restored archive material, Google Drive material, credentials, and Colab outputs
remain excluded from source control.

The M16.7 combined stance is:

```text
notebook_13_runtime_smoke_verified_without_committed_outputs
```

Claim boundaries remain unchanged: preview/preflight evidence is not native
campaign execution evidence; artifact discovery alone does not prove
current-session execution; governance rows were 0, so no governance readiness
claim is made; split metric rows were 0, so no split-metric completeness claim
is made; and Notebook 13 still makes no production, strategy approval,
promotion, statistical significance, alpha validation, upstream-template, or
source/runtime equivalence claim.

## Static Coverage Summary

Issue #128 added source-only Notebook 13 static coverage:

- `tests/test_notebook_13_source_contracts.py`
- `tests/test_notebook_13_execution_guardrails.py`
- `tests/test_notebook_13_artifact_handoff_contracts.py`

Issue #129 strengthened the notebook and these tests around generated config
provenance, catalog readiness, strategy resolution, alpha fallback, execution
blockers, caveat preservation, and handoff boundaries.

The tests parse committed source files only. They do not execute notebook cells,
import StratLake runtime packages as a requirement, call native CLI commands,
mount Drive, restore archives, generate campaign configs, write runtime
artifacts, depend on Colab, depend on network access, or depend on secrets.

## Validation History

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

This is local validation evidence. Remote CI evidence should be recorded
separately when available.

## Non-Claims

The committed Notebook 13 source and this audit do not claim:

- Production readiness.
- Strategy approval.
- Promotion readiness.
- Governance readiness without native governance evidence.
- Statistical significance.
- Alpha validation.
- Generated configs are upstream native templates.
- Runtime smoke evidence is committed notebook output.
- Source-only validation is equivalent to live Colab/manual runtime validation.

Completion stance:

```text
notebook_13_runtime_smoke_verified_without_committed_outputs
```

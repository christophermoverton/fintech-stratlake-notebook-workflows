# Notebook 12 Command Surface Classification

## Purpose

Notebook 12 (`notebooks/12_stratlake_campaign_evidence_gap_promotion_readiness.ipynb`)
is a source-safe campaign evidence gap review and human-review handoff notebook.
It previews, inspects, classifies, summarizes, and hands off campaign evidence
surfaces. It does not replace native StratLake campaign execution,
orchestration, manifests, run registries, metrics, split metrics, promotion
gates, checkpoint/retry/reuse records, or promotion decisions.

This classification does not prove live package installation, Drive access,
credential availability, archive restore, native campaign execution, campaign
artifact completeness, alpha, strategy approval, statistical significance,
production readiness, promotion governance success, or promotion-grade
readiness.

## Source And Runtime Posture

| Property | Value |
|---|---|
| Target notebook | `notebooks/12_stratlake_campaign_evidence_gap_promotion_readiness.ipynb` |
| Source posture | Cleaned, output-free, execution-count-null, metadata-minimized |
| Runtime posture | Live/manual Colab or prepared local notebook execution only |
| Committed default profile | `cold_smoke_5_command_shape_readiness` |
| Baseline preview profile | `cold_smoke_1_preview` |
| Manual campaign-smoke mode | `campaign_smoke_run` |

## Classification Legend

| Category | Meaning |
|---|---|
| `source_only` | Source text, notebook JSON, metadata, references, and guards can be inspected without runtime execution. |
| `preview_only` | Builds or displays command/config/review intent without executing native campaign work. |
| `live_manual` | Requires deliberate live notebook execution in Colab or another prepared runtime. |
| `guarded_runtime` | Runtime action is protected by a profile, boolean gate, dry-run requirement, placeholder guard, or manual enablement. |
| `runtime_validation` | Depends on restored paths, CLI availability, configs, help text, or generated runtime rows. |
| `artifact_review` | Discovers, writes, inventories, filters, or interprets generated runtime artifacts. |
| `campaign_evidence_review` | Interprets campaign evidence sufficiency and blockers without approving strategies or promotions. |
| `out_of_ci_scope` | Must not be required by repository validation or CI. |

## Profile Classification

| Profile | Notebook use | Classification | Execution boundary |
|---|---|---|---|
| `cold_smoke_1_preview` | Baseline source-safe preview with no restore, campaign discovery, campaign run, evidence run, governance run, or checkpoint. | `source_only`, `preview_only` | No native campaign execution. |
| `cold_smoke_5_command_shape_readiness` | Committed import default. Checks command shapes and discovery surfaces while keeping execution disabled. | `source_only`, `preview_only`, `runtime_validation` | May inspect command availability/help shape in live runtime; does not execute native campaign smoke. |
| `campaign_smoke_preview` | Prepares or discovers a campaign smoke config and previews the native run command. | `preview_only`, `guarded_runtime`, `runtime_validation` | Does not execute; generated configs remain review aids. |
| `campaign_smoke_dry_run` | Guarded native campaign smoke dry run. | `live_manual`, `guarded_runtime`, `runtime_validation`, `out_of_ci_scope` | Executes only when profile/controls allow execution and the native CLI advertises a recognized dry-run option. |
| `campaign_smoke_dry_run_allow_provisional` | Allows a validated Notebook 12-generated provisional config for dry-run execution. | `live_manual`, `guarded_runtime`, `runtime_validation`, `out_of_ci_scope` | Still dry-run only; provisional config must remain classified as `notebook12_generated_smoke_config`, not a native template. |
| `campaign_smoke_execute_allow_provisional_no_dry_run` | Explicit non-dry-run tiny native campaign smoke using a validated provisional config. | `live_manual`, `guarded_runtime`, `runtime_validation`, `artifact_review`, `out_of_ci_scope` | Deliberate opt-in only; requires explicit non-dry-run profile/control and remains non-claiming. |

## Command And Runtime Surfaces

| Surface | Notebook use | Classification | Source-only validation boundary |
|---|---|---|---|
| Dependency install cell | Installs runtime dependencies in live notebook sessions. | `live_manual`, `out_of_ci_scope` | Verify command shape only; do not install packages in repository validation. |
| Imports, Colab detection, display helpers | Provides source/runtime helpers for display, subprocess, JSON, DataFrame, and Colab detection. | `source_only`, `runtime_validation` | Import/source text can be inspected; runtime helper behavior is manual. |
| Runtime controls and `NOTEBOOK12_TEST_PROFILE` | Central profile selector and boolean control table. | `source_only`, `guarded_runtime` | Verify committed default is `cold_smoke_5_command_shape_readiness` and guards remain conservative. |
| Colab, Google Drive, workspace path setup | Mounts Drive and configures notebook workspace paths in live sessions. | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Verify path placeholders and guard language only; do not mount Drive in CI. |
| Session archive root discovery | Finds or reports candidate archive roots for manual restore/review. | `runtime_validation`, `artifact_review` | Paths are optional during source validation. |
| CLI/import availability checks | Checks commands such as `stratlake-run-research-campaign`, evidence review, governance report, and archive helpers. | `runtime_validation`, `preview_only` | Verify command names and help/availability probes; do not require installed CLIs in CI. |
| Fintech session initialization | Initializes or attaches the Fintech project/session structure. | `live_manual`, `guarded_runtime`, `runtime_validation` | Verify command construction only. |
| StratLake session initialization | Initializes or attaches the StratLake workspace/session. | `live_manual`, `guarded_runtime`, `runtime_validation` | Verify command construction only; no campaign execution implied. |
| Guarded native campaign smoke path | Builds preview/execution conditions for `stratlake-run-research-campaign`. | `preview_only`, `live_manual`, `guarded_runtime`, `runtime_validation`, `out_of_ci_scope` | Execution is off unless profile/controls allow it; dry-run guard remains active by default. |
| Generated provisional campaign smoke config | Writes a Notebook 12 reference smoke config for human inspection or explicitly allowed dry-run smoke. | `artifact_review`, `guarded_runtime`, `runtime_validation`, `out_of_ci_scope` | Must be classified as `notebook12_generated_smoke_config`; never as a native template. |
| Dry-run detection and blocking behavior | Detects advertised dry-run options and blocks dry-run execution when none are available. | `guarded_runtime`, `runtime_validation` | Missing dry-run support is a blocking status, not permission to run live. |
| Optional archive restore | Restores selected session archives only when explicitly enabled. | `live_manual`, `guarded_runtime`, `artifact_review`, `out_of_ci_scope` | Verify false default and command shape; do not restore archives in tests. |
| Notebook 11 context discovery | Loads Notebook 11 expanded-review context when requested. | `runtime_validation`, `artifact_review`, `campaign_evidence_review` | Context is prior review evidence only; it is not native campaign context by itself. |
| Campaign artifact discovery | Discovers candidate campaign artifacts from configured roots. | `artifact_review`, `runtime_validation`, `campaign_evidence_review` | Missing artifacts produce caveats/statuses, not success. |
| Native campaign artifact filtering | Separates native campaign-looking artifacts from Notebook 12 review artifacts and applies strict campaign/run filters when configured. | `artifact_review`, `runtime_validation`, `campaign_evidence_review` | Notebook 12 must not fabricate campaign context from its own review artifacts. |
| Notebook 12 review artifact separation | Keeps notebook-generated review outputs visible for audit but excluded from native campaign context unless real native campaign markers are present. | `artifact_review`, `campaign_evidence_review` | `notebook12_review_artifact_rows` and `native_campaign_artifact_rows` remain distinct. |
| Campaign evidence dataframe and sufficiency classification | Builds candidate rows and conservative sufficiency labels for human review. | `artifact_review`, `campaign_evidence_review` | Sufficiency is a review classification, not strategy approval or promotion readiness certification. |
| Governance/evidence/report CLI command previews | Previews campaign report, evidence review, and promotion governance command shapes. | `preview_only`, `runtime_validation`, `guarded_runtime` | Preview/schema inspection only unless manually enabled; no promotion decision is made. |
| Caveat register | Records missing campaign context, missing native evidence, missing dry-run support, incomplete promotion evidence, and disabled execution. | `campaign_evidence_review`, `artifact_review` | Missing context/evidence remains a caveat or blocker, not hidden success. |
| Notebook 12 review artifact writing | Writes `summary.json`, smoke result, inventory CSVs, evidence review CSV, caveat register, and final handoff under the Notebook 12 review directory. | `artifact_review`, `out_of_ci_scope` | Generated runtime outputs stay out of Git. |
| Optional archive checkpoint | Creates a runtime archive checkpoint only when explicitly enabled. | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Verify false default and command shape; do not checkpoint in tests. |
| Final handoff | Summarizes source/runtime posture, campaign artifact counts, evidence status counts, caveats, non-claims, and next actions. | `source_only`, `artifact_review`, `campaign_evidence_review` | Handoff remains descriptive and conservative; no approval or production-readiness claim. |

## Guarded Controls

Notebook 12 source defaults remain conservative:

```python
NOTEBOOK12_TEST_PROFILE = "cold_smoke_5_command_shape_readiness"
NOTEBOOK12_MODE = "campaign_preview"
RUN_STRATLAKE_ARCHIVE_RESTORE = False
DISCOVER_NOTEBOOK11_EXPANDED_CONTEXT = False
DISCOVER_CAMPAIGN_CONTEXT = False
RUN_CAMPAIGN_ARTIFACT_DISCOVERY = False
RUN_CAMPAIGN_EVIDENCE_REVIEW = False
RUN_CAMPAIGN_GOVERNANCE_REVIEW = False
RUN_STRATLAKE_CAMPAIGN_REPORT = False
RUN_STRATLAKE_ARCHIVE_CHECKPOINT = False
RUN_NATIVE_CAMPAIGN_SMOKE = False
ALLOW_NATIVE_CAMPAIGN_SMOKE_EXECUTION = False
NATIVE_CAMPAIGN_SMOKE_DRY_RUN_ONLY = True
REQUIRE_DRY_RUN_ARGUMENT_FOR_NATIVE_CAMPAIGN_SMOKE = True
ALLOW_NON_DRY_RUN_NATIVE_CAMPAIGN_SMOKE_EXECUTION = False
ALLOW_PROVISIONAL_CAMPAIGN_SMOKE_CONFIG_FOR_EXECUTION = False
VALIDATE_PROVISIONAL_CAMPAIGN_SMOKE_CONFIG = True
RUN_ID_STRICT_PLATFORM_ARTIFACT_DISCOVERY = True
ALLOW_REFERENCE_ONLY_CAMPAIGN_PLAN = False
DISCOVER_EXISTING_CAMPAIGN_ARTIFACTS = False
REQUIRE_CAMPAIGN_OR_RUN_FILTER_FOR_RESTORED_REVIEW = False
```

The default-profile clarification is intentional: earlier draft markdown called
`cold_smoke_1_preview` the default, but committed source defaults to
`cold_smoke_5_command_shape_readiness`. That profile is still source-safe
because native campaign execution remains disabled.

## Native StratLake Boundary

Native StratLake remains the source of truth for campaign execution, campaign
orchestration, manifests, run registries, metrics, split metrics, promotion
gates, checkpoint/retry/reuse behavior, campaign reports, and promotion
decisions. Notebook 12 may preview commands, inspect restored artifacts,
classify evidence sufficiency, register caveats, and hand off next actions.

Notebook 12 must not fabricate campaign context from its own review artifacts.
Notebook-generated smoke configs must remain marked as
`notebook12_generated_smoke_config`; true native templates are reported
separately as native campaign templates.

## Non-Claims

Notebook 12 source must not claim strategy approval, alpha validation,
production readiness, statistical significance, complete platform artifact
coverage, promotion governance success, or promotion-grade readiness. Missing
campaign context or missing promotion evidence should be documented as caveats,
blockers, or next actions.

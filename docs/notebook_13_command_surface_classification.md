# Notebook 13 Command And Runtime Surface Classification

## Purpose

Notebook 13
(`notebooks/13_stratlake_native_campaign_execution_and_artifact_generation.ipynb`)
is a source-safe native campaign execution and artifact generation notebook. It
continues Notebook 12 by moving from campaign evidence gap review into guarded
native StratLake campaign execution, artifact inventory, caveat registration,
and Notebook 12-compatible handoff.

Notebook 13 composes existing StratLake command surfaces. It does not replace
native StratLake campaign orchestration, strategy execution, manifests, run
registries, metrics, split metrics, reporting, governance, archive restore, or
archive checkpoint behavior. Native StratLake remains the source of truth for
those surfaces.

This classification does not prove live package installation, Colab/Drive
availability, credential availability, archive restore, native campaign
execution, artifact completeness, governance readiness, strategy approval,
alpha validation, statistical significance, production readiness, promotion
readiness, or CI/runtime equivalence.

## Source And Runtime Posture

| Property | Value |
|---|---|
| Issue | #127 - M16.2 - Classify Notebook 13 Runtime Gates, Restore, Config, and Native Execution Surfaces |
| Depends on | #126 - M16.1 - Stage and Clean Notebook 13 Native Campaign Execution Workflow |
| Target notebook | `notebooks/13_stratlake_native_campaign_execution_and_artifact_generation.ipynb` |
| Source posture | Cleaned, output-free, execution-count-null |
| Runtime posture | Live/manual Colab or prepared local notebook execution only |
| Committed default profile | `campaign_execution_preview` |
| Manual preflight profile | `campaign_execution_preflight` |
| Manual native execution profile | `campaign_execution_run` |
| Optional archive checkpoint profile | `campaign_execution_run_with_archive_checkpoint` |
| Runtime artifact root | `artifacts/notebook_13_native_campaign_execution_and_artifact_generation/` |

The companion runtime review recorded a successful external smoke run with
`stratlake-run-research-campaign` returning code 0 and native campaign artifacts
detected. That smoke evidence is runtime context only. It is not committed
notebook output and does not alter the source-safe default posture.

## Classification Legend

| Category | Meaning |
|---|---|
| `source_only` | Source text, notebook JSON, metadata, references, and guards can be inspected without runtime execution. |
| `preview_only` | Builds, displays, or records command/config/review intent without executing native campaign work. |
| `live_manual` | Requires deliberate live notebook execution in Colab or another prepared runtime. |
| `guarded_runtime` | Runtime action is protected by a profile flag, boolean gate, reviewed-input gate, or manual enablement. |
| `restore_dependent` | Depends on restored session material under the active StratLake workspace. |
| `generated_config_dependent` | Depends on notebook-generated execution-candidate configs or user-supplied/native configs. |
| `native_execution_dependent` | Depends on `stratlake-run-research-campaign` or another native StratLake command actually running. |
| `runtime_validation` | Depends on CLI availability, help text, restored files, configs, feature roots, or runtime paths. |
| `artifact_review` | Discovers, writes, inventories, previews, or interprets generated runtime artifacts. |
| `handoff` | Produces Notebook 12-compatible downstream review context and next-action status. |
| `out_of_ci_scope` | Must not be required by repository validation or CI. |

## Profile Classification

| Profile | Notebook use | Enabled profile flags | Classification | Execution boundary |
|---|---|---|---|---|
| `campaign_execution_preview` | Committed source-safe default. Discovers command/config surfaces and runs command/input preflight with execution disabled. | `DISCOVER_NATIVE_COMMANDS`, `DISCOVER_CAMPAIGN_CONFIGS`, `RUN_CAMPAIGN_PREFLIGHT`, `WRITE_NOTEBOOK13_SUMMARY_ARTIFACTS` | `source_only`, `preview_only`, `runtime_validation` | Does not restore archives or execute native campaigns by default. |
| `campaign_execution_preflight` | Manual restore/input-readiness and command-shape preflight profile. | Adds Fintech/StratLake session init and `RUN_ARCHIVE_RESTORE`; keeps `RUN_NATIVE_CAMPAIGN_EXECUTION` false. | `live_manual`, `guarded_runtime`, `restore_dependent`, `runtime_validation`, `out_of_ci_scope` | Restore remains blocked unless `NOTEBOOK13_ALLOW_ARCHIVE_RESTORE=true`; no native campaign execution. |
| `campaign_execution_run` | Manual full native campaign execution profile. | Adds `RUN_NATIVE_CAMPAIGN_EXECUTION`, optional report commands, and optional governance commands. | `live_manual`, `guarded_runtime`, `restore_dependent`, `generated_config_dependent`, `native_execution_dependent`, `artifact_review`, `out_of_ci_scope` | Execution also requires `NOTEBOOK13_ALLOW_NATIVE_EXECUTION=true`, successful preflight, reviewed inputs, and generated-config allow gates when generated configs are selected. |
| `campaign_execution_run_with_archive_checkpoint` | Full native campaign execution plus native archive checkpoint. | Same as run profile plus `RUN_ARCHIVE_CHECKPOINT`. | `live_manual`, `guarded_runtime`, `native_execution_dependent`, `artifact_review`, `out_of_ci_scope` | Checkpoint also requires `NOTEBOOK13_ALLOW_ARCHIVE_CHECKPOINT=true`; generated checkpoint outputs stay outside Git. |

## Runtime Gates

Notebook 13 source defaults are conservative:

```python
NOTEBOOK13_TEST_PROFILE = "campaign_execution_preview"
NOTEBOOK13_ALLOW_NATIVE_EXECUTION = False
NOTEBOOK13_ALLOW_ARCHIVE_RESTORE = False
NOTEBOOK13_ALLOW_ARCHIVE_CHECKPOINT = False
NOTEBOOK13_ALLOW_NOTEBOOK_GENERATED_CONFIG_EXECUTION = False
NOTEBOOK13_MARK_INPUTS_USER_REVIEWED = False
```

The effective workspace initialization profile flag in the committed notebook is
`RUN_STRATLAKE_SESSION_INIT`. The manual companion recipes refer to
`RUN_STRATLAKE_INIT`; documentation should treat workspace initialization as a
manual/profile-controlled setup surface and source validation should inspect the
actual profile flag present in the notebook source.

| Gate | Surface controlled | Default/source posture | Runtime boundary |
|---|---|---|---|
| `RUN_STRATLAKE_SESSION_INIT` / `RUN_STRATLAKE_INIT` recipe intent | StratLake notebook/session workspace initialization. | Disabled in `campaign_execution_preview`; enabled by manual preflight/run profiles. | Initializes workspace only; does not imply archive restore or campaign execution. |
| `NOTEBOOK13_ALLOW_ARCHIVE_RESTORE` | `stratlake-session-archive-restore-bootstrap`. | False. | Restore requires a profile requesting restore and this allow flag. |
| `NOTEBOOK13_CREATE_EXECUTION_CONFIGS` | Generated execution-candidate campaign/universe config creation. | Optional and manually enabled. | Generated configs are review candidates, not canonical upstream templates. |
| `NOTEBOOK13_MARK_INPUTS_USER_REVIEWED` | Marks selected native/user-supplied/generated runtime inputs as reviewed. | False. | Native execution input readiness remains false until reviewed inputs are marked or specific reviewed flags are supplied. |
| `NOTEBOOK13_ALLOW_NOTEBOOK_GENERATED_CONFIG_EXECUTION` | Allows selected notebook-generated execution-candidate configs to be used for native execution. | False. | Required only after human review when generated campaign/universe configs are selected. |
| `NOTEBOOK13_ALLOW_NATIVE_EXECUTION` | Enables native campaign and optional report/governance command execution when a run profile requests it. | False. | Native command execution remains blocked without this flag even in `campaign_execution_run`. |
| `NOTEBOOK13_ALLOW_ARCHIVE_CHECKPOINT` | Enables post-run archive checkpointing. | False. | Checkpoint remains manual and profile-gated. |

## Command And Runtime Surfaces

| Surface | Notebook use | Classification | Source-only validation boundary |
|---|---|---|---|
| Dependency install cell | Installs `stratlake-trade-engine` using the TestPyPI/PyPI fallback pattern in a live notebook runtime. | `live_manual`, `out_of_ci_scope` | Verify source command shape only; do not install packages in repository validation. |
| Imports, helpers, Colab/local detection | Provides defensive display, subprocess, JSON, DataFrame, and environment helpers. | `source_only`, `runtime_validation` | Source can be inspected without Colab or installed native CLIs. |
| Runtime profile selector | Defines `campaign_execution_preview`, `campaign_execution_preflight`, `campaign_execution_run`, and `campaign_execution_run_with_archive_checkpoint`. | `source_only`, `guarded_runtime` | Verify default remains `campaign_execution_preview` and execution gates default false. |
| Workspace path setup | Establishes `/content`, `/content/stratlake`, Drive archive roots, and notebook artifact roots in live runtime. | `live_manual`, `guarded_runtime`, `out_of_ci_scope` | Path references are source-visible; runtime folders and Drive contents are not committed. |
| StratLake workspace initialization | Prefers `stratlake-init-notebook --root /content/stratlake`, with `stratlake-init-session` fallback/session behavior when advertised and shapeable. | `live_manual`, `guarded_runtime`, `runtime_validation`, `out_of_ci_scope` | Initialization is notebook workspace setup, not native campaign execution. |
| Native command discovery | Checks command availability, help text, entry points, and import surfaces for native and optional commands. | `runtime_validation`, `preview_only` | Missing commands/modules become caveats; CI/source checks must not require installed native CLIs. |
| Archive restore | Uses `stratlake-session-archive-restore-bootstrap` to restore archived session material before config discovery. | `live_manual`, `guarded_runtime`, `restore_dependent`, `artifact_review`, `out_of_ci_scope` | Verify command shape and false allow default; do not restore archives in repository validation. |
| Generated starter configs | Creates preview/starter scaffolds for command-shape validation. | `preview_only`, `generated_config_dependent`, `runtime_validation` | Starter scaffolds are source/runtime aids and must not be called native templates. |
| Generated execution-candidate campaign config | Writes a notebook-generated native `research_campaign` execution-candidate config using reviewed runtime inputs. | `guarded_runtime`, `generated_config_dependent`, `runtime_validation`, `out_of_ci_scope` | Config source remains `notebook13_generated_execution_candidate_config`, not a canonical upstream StratLake template. |
| Generated universe config | Writes a notebook-generated execution-candidate universe config when no reviewed/user-provided universe config is selected. | `guarded_runtime`, `generated_config_dependent`, `runtime_validation`, `out_of_ci_scope` | Requires review before execution; generated provenance remains explicit. |
| Strategy/catalog readiness | Checks restored `/content/stratlake/configs/strategies.yml`, `/content/stratlake/configs/portfolios.yml`, optional `/content/stratlake/configs/alphas.yml`, aliases, defaults, and blockers. | `restore_dependent`, `runtime_validation`, `generated_config_dependent` | Missing strategies or requested alpha targets without a real alpha catalog are blockers, not caveats to ignore. |
| Strategy-only empty alpha catalog fallback | Generates an empty notebook-local alpha catalog only when no alpha targets are requested and no real alpha catalog exists. | `guarded_runtime`, `generated_config_dependent`, `runtime_validation` | This is a strategy-only fallback. Requested alpha targets still require a real alpha catalog. |
| Native command preflight | Builds and inspects `stratlake-run-research-campaign --config <config>` command shape. | `preview_only`, `runtime_validation`, `generated_config_dependent` | Preflight validates command shape and inputs; it does not claim campaign execution. |
| Input readiness preflight | Checks campaign config, universe config, feature input root, reviewed-input status, generated-config allow status, and blockers. | `runtime_validation`, `guarded_runtime`, `generated_config_dependent` | Missing or unreviewed inputs block native execution. |
| Native campaign execution | Runs `stratlake-run-research-campaign --config <config>`. | `live_manual`, `guarded_runtime`, `native_execution_dependent`, `artifact_review`, `out_of_ci_scope` | Requires run profile, `NOTEBOOK13_ALLOW_NATIVE_EXECUTION=true`, successful preflight, reviewed inputs, and no blockers. Success is claimed only when return code is 0. |
| Artifact discovery | Inventories native campaign artifacts, notebook summary artifacts, generated candidate configs, restored session inputs, and candidate campaign context. | `artifact_review`, `runtime_validation`, `native_execution_dependent` | Discovery may find prior runtime artifacts; it must record whether Notebook 13 executed in the current session. |
| Artifact preview/loading | Performs shallow manifest, run registry, metrics, split metrics, governance, report, and handoff previews. | `artifact_review`, `runtime_validation` | Filename presence is not promotion evidence; metrics are not recomputed. |
| Optional report/evidence/governance commands | Discovers/builds optional commands such as `stratlake-build-campaign-report`, `stratlake-build-evidence-review`, and `stratlake-run-promotion-governance-report`. | `live_manual`, `guarded_runtime`, `runtime_validation`, `artifact_review`, `out_of_ci_scope` | Commands run only when the run profile enables the surface and `NOTEBOOK13_ALLOW_NATIVE_EXECUTION=true`; unavailable commands become caveats. |
| Archive checkpoint | Runs native archive checkpointing through `stratlake-session-archive-bootstrap` when retained and explicitly enabled. | `live_manual`, `guarded_runtime`, `artifact_review`, `out_of_ci_scope` | Requires checkpoint profile and `NOTEBOOK13_ALLOW_ARCHIVE_CHECKPOINT=true`; checkpoint payloads stay outside Git. |
| Caveat register | Records preflight blockers, restore caveats, execution blockers, optional command caveats, checkpoint caveats, missing governance, and non-claim boundaries. | `artifact_review`, `handoff`, `runtime_validation` | Caveats are evidence-preserving and prevent overstated readiness. |
| Execution summary and handoff | Writes `campaign_execution_summary.json` and `campaign_execution_handoff.json` under the notebook artifact root during runtime. | `artifact_review`, `handoff`, `out_of_ci_scope` | Handoff summarizes what actually happened; generated summaries are not committed notebook output. |

## Archive Restore Surface

Restore is a guarded/manual runtime surface. The current preferred command shape
is:

```text
stratlake-session-archive-restore-bootstrap \
  --archive-root <Google Drive/session archive root>/<archive-id> \
  --target-root /content/stratlake \
  --validate-before-restore \
  --inspect-before-restore \
  --overwrite-policy overwrite_allowed
```

The archive source is the Google Drive/session archive root, usually under
`/content/drive/MyDrive/stratlake-colab/session_archives`. The restore target is
the local StratLake workspace, usually `/content/stratlake`. Drive remains the
archive/session persistence location and must not become the active app
workspace.

Restore requires both a profile that requests restore and
`NOTEBOOK13_ALLOW_ARCHIVE_RESTORE=true`. Repository validation may inspect the
command construction and guard defaults, but must not restore archives, require
Google Drive, or commit restored session files.

## Generated Config Provenance

Notebook 13 may generate native-loadable execution candidates when deliberately
enabled, but those files remain notebook-generated artifacts:

- `notebook13_generated_execution_candidate_config`
- `notebook13_generated_execution_candidate_universe`
- notebook-local empty alpha catalog fallback for strategy-only campaigns

Generated configs use the native `research_campaign` schema so they can be
preflighted and, after review, executed by the native command. They are not
canonical upstream StratLake templates and must not be documented as such.
Their source metadata and comments should preserve `notebook-generated`,
`execution-candidate`, `native_template: false`,
`requires_user_review_before_execution: true`, and generated-config execution
allow requirements.

Executing a generated campaign or universe config requires:

- the relevant run/preflight profile,
- `NOTEBOOK13_MARK_INPUTS_USER_REVIEWED=true` or equivalent reviewed-input
  flags,
- `NOTEBOOK13_ALLOW_NOTEBOOK_GENERATED_CONFIG_EXECUTION=true`,
- successful native command/input preflight,
- and, for actual execution, `NOTEBOOK13_ALLOW_NATIVE_EXECUTION=true`.

## Strategy And Catalog Readiness

Notebook 13 checks native/restored catalog readiness before allowing execution.
The expected restored paths are:

- `/content/stratlake/configs/strategies.yml`
- `/content/stratlake/configs/portfolios.yml`
- `/content/stratlake/configs/alphas.yml`, when real alpha targets are requested

Strategy alias/default handling allows common short names to resolve to native
catalog names such as `momentum_v1`. Unresolved requested strategies are hard
blockers.

Preflight and handoff summaries should carry requested strategies, resolved
strategies, alias/default substitutions, unknown strategies, catalog readiness
blockers, and any strategy-resolution caveats so fallback behavior remains
visible to reviewers.

Alpha catalog handling is intentionally conservative. If no alpha targets are
requested and no real alpha catalog exists, Notebook 13 may generate a
notebook-local empty alpha catalog for a strategy-only campaign. If alpha
targets are requested, a missing real alpha catalog is a hard blocker.
The fallback is not alpha readiness, alpha validation, promotion evidence, or a
substitute for a real alpha catalog when `NOTEBOOK13_CAMPAIGN_ALPHAS` requests
alpha targets.

## Artifact And Handoff Boundaries

Notebook 13 can discover or write several runtime artifact classes:

- native campaign artifacts,
- notebook summary artifacts,
- generated execution-candidate configs,
- restored session inputs,
- candidate campaign context,
- caveat register rows,
- execution summaries,
- Notebook 12-compatible handoff summaries.

These runtime outputs belong under runtime artifact roots such as
`artifacts/notebook_13_native_campaign_execution_and_artifact_generation/` or
the active StratLake workspace. They must stay out of Git unless a future issue
explicitly documents a source artifact. Committed notebook source must remain
output-free and execution-count-null.

Artifact discovery is not itself proof of current-session execution. The
execution summary must remain the source for whether Notebook 13 actually ran
`stratlake-run-research-campaign` in the current session, and success should be
claimed only when the native return code is 0.
Handoff summaries should preserve execution requested/enabled/status/succeeded
fields, execution blockers, catalog/strategy/alpha blockers, caveats, and
explicit non-claim flags.

## Optional Governance, Reporting, And Checkpoint Surfaces

Optional report, evidence-review, governance, and archive checkpoint surfaces
remain manual and guarded:

- `stratlake-build-campaign-report`
- `stratlake-build-evidence-review`
- `stratlake-run-promotion-governance-report`
- `stratlake-session-archive-bootstrap`

Notebook 13 may discover help text, build command shapes, record unavailable
commands as caveats, and run optional commands only in an explicitly enabled
live runtime. Missing governance rows or unavailable governance commands must
remain caveats and must not be converted into governance-readiness claims.

## Source-Only Validation Boundary

Repository validation for M16.2 may inspect:

- notebook JSON parseability,
- output-free and execution-count-null source state,
- default `campaign_execution_preview` posture,
- runtime profile names and conservative gates,
- native command references,
- restore command shape,
- generated config provenance labels,
- strategy/catalog blocker language,
- artifact origin and handoff fields,
- non-claim flags and caveat language,
- documentation source safety.

Repository validation must not execute notebook cells, install packages, mount
Google Drive, prompt for credentials, initialize Fintech or StratLake sessions,
restore archives, generate campaign configs as committed artifacts, run native
campaigns, run governance/reporting commands, checkpoint archives, write runtime
artifacts, or treat external smoke evidence as committed notebook output.

## Non-Claims

Notebook 13 source must not claim:

- production readiness,
- strategy approval,
- promotion readiness,
- governance readiness unless native governance evidence exists,
- statistical significance,
- generated configs are native upstream templates,
- runtime smoke evidence is committed notebook output,
- CI/source validation is equivalent to Colab/manual runtime validation,
- artifact discovery alone proves current-session native execution.

Completion stance for this classification issue:
`notebook_13_runtime_surfaces_classified_source_safe`.

# Colab Smoke-Test Workflow

## Purpose

Use this workflow for final manual Colab validation after local notebook checks pass. Local checks can validate repository cleanliness, static syntax, sanitized execution, and CLI contract drift, but they cannot fully prove Colab runtime behavior.

Colab-specific behavior includes runtime package installation, shell command behavior, `/content` filesystem behavior, Google Drive mounting, Colab Secrets, and notebook display behavior. These should be smoke-tested manually before a notebook is treated as run-ready.

## Validation Layers

Use the layers in this order:

1. Static repository guardrails:

   ```bash
   python scripts/scan_for_secret_patterns.py .
   python scripts/check_notebooks_no_outputs.py notebooks
   python scripts/validate_repo_cleanliness.py .
   ```

2. Execution-readiness checks:

   ```bash
   python scripts/validate_notebook_execution_readiness.py --config config/notebook_test.toml
   ```

3. Sanitized pytest notebook execution:

   ```bash
   pytest
   ```

4. CLI contract validation:

   ```bash
   python scripts/validate_notebook_cli_contracts.py --config config/notebook_cli_contracts.toml
   ```

5. Manual Colab smoke validation using a fresh runtime.

Automated local checks must not run real ingestion, archive writes, restore writes, Drive mounts, credential prompts, live API calls, StratLake feature generation, strategy execution, backtests, or artifact-producing workflows.

## Fresh Runtime Checklist

1. Open the notebook in Google Colab.
2. Restart the runtime before testing.
3. Run setup and package-install cells that the notebook expects for Colab.
4. Confirm expected native CLI commands are available with `--help`.
5. Run dry-run command cells only where the notebook explicitly marks them as dry-run previews.
6. Confirm no real ingestion, archive write, restore write, feature generation, strategy execution, backtest, or artifact generation occurs unless the notebook explicitly intends that workflow.
7. Confirm active work uses `/content`.
8. Confirm Google Drive is used only for persistence, backup, archive, and restore storage.
9. Confirm Colab Secrets or safe prompts are used for credentials.
10. Capture CLI errors in an issue comment or local notes, not in committed notebook outputs.
11. Fix the notebook and rerun the smoke path when errors are found.
12. Clear all outputs and reset execution counts before commit.
13. Run local validation commands again before final commit or audit.

## CLI Error Handling

If a CLI command fails in Colab:

- Do not commit the traceback or command output.
- Record the command, expected behavior, observed error, and package version in a local note or issue comment.
- Decide whether the fix belongs in the notebook workflow repository or upstream in `fintech-market-ingestion` or `stratlake-trade-engine`.
- Keep notebook changes limited to orchestration, validation, parsing, display, review, and human-readable workflow guidance.

## Output Cleanup

After smoke testing:

- Clear all cell outputs.
- Reset or remove execution counts where practical.
- Inspect raw `.ipynb` JSON.
- Confirm no generated data, archives, restore packs, local workspaces, runtime folders, notebook outputs, embedded blobs, private paths, or secrets are present.
- Run local repository validation commands.

Colab logs, screenshots, tracebacks, Drive listings, command outputs, and generated artifacts should not be committed.

## Boundary Reminder

Manual Colab smoke testing verifies notebook runnability in the intended runtime. It does not change the repository boundary: notebooks orchestrate, validate, parse, display, and review upstream behavior. They should not reimplement native Fintech ingestion, StratLake feature generation, archive/restore, strategy, backtest, or artifact logic.

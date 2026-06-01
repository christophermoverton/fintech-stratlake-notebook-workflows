---
name: Notebook audit
about: Audit a Colab notebook for safety, consistency, runnability, and native-command-first behavior
title: "Notebook Audit - "
labels: notebooks, audit
assignees: ""
---

## Description

Describe the notebook audit request and the reason this notebook is ready for review.

## Notebook

- Notebook filename:
- Planned sequence number:
- Related workflow step:

## Context

- Source location before import:
- Related milestone or issue:
- Upstream apps involved:
  - [ ] `fintech-market-ingestion`
  - [ ] `stratlake-trade-engine`

## Audit Scope

- [ ] Notebook filename follows the documented standards.
- [ ] Required header metadata exists near the top of the notebook.
- [ ] Purpose, runtime, upstream apps, path variables, native commands, generated outputs, and commit safety are documented.
- [ ] Notebook is runnable in the expected Colab context.

## Secret Safety

- [ ] No hardcoded Alpaca API keys.
- [ ] No hardcoded Alpaca secret keys.
- [ ] No bearer tokens, private keys, credential files, or local runtime secrets.
- [ ] No printed `os.environ`.
- [ ] Credential access uses Colab Secrets or hidden prompt fallback.

## Notebook Output Safety

- [ ] Cell outputs are cleared.
- [ ] Execution counts are reset or removed where practical.
- [ ] No tracebacks, logs, API responses, tables, or large embedded output blobs remain.
- [ ] No output text contains credential-looking names or values.

## Colab and Google Drive Path Behavior

- [ ] Active Colab work stays under `/content`.
- [ ] Google Drive usage is limited to persistence, archive packs, backups, and restore workflows.
- [ ] Drive is not used as the active app workspace unless the notebook documents a safe reason.
- [ ] Paths are portable where practical.

## Native Command First Review

- [ ] Native CLI commands are used where available.
- [ ] Notebook code orchestrates, validates, parses, displays, and reviews outputs.
- [ ] Notebook code does not reimplement native ingestion, archive/restore, feature generation, strategy, backtest, or artifact logic.

## Generated Output Boundary

- [ ] No generated data or archive files are staged.
- [ ] No restore packs are staged.
- [ ] No local app workspaces are staged.
- [ ] No Google Drive runtime folders are staged.
- [ ] Expected generated outputs are documented as runtime artifacts that must not be committed.

## Acceptance Criteria

- [ ] Notebook is safe to import into `notebooks/`.
- [ ] Notebook follows naming and metadata standards.
- [ ] Repository boundary is respected.
- [ ] Manual review and validation scripts pass.

## Validation

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
```

## Notes

Add reviewer notes, follow-up items, or upstream triage links.

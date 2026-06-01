# Notebook Import Staging Guide

## Purpose

This guide defines the process for preparing existing Colab notebooks before moving them from Google Drive into this repository. Notebook imports should happen through controlled staging, classification, cleanup, validation, and review, not by directly copying Google Drive notebooks into `notebooks/`.

## When to Use This Guide

Use this guide before importing any existing Colab notebook from Google Drive, local downloads, backups, archives, or prior runtime sessions. Existing notebooks should remain outside the repository until they are classified, cleaned, reviewed, and validated.

This issue does not import Notebook 00 through Notebook 09 or any other actual notebooks.

## Staging Principles

- Do not copy notebooks directly from Google Drive into `notebooks/`.
- Use a temporary staging area first.
- Treat staged notebooks as untrusted until reviewed.
- Do not commit staging folders.
- Keep active Colab work under `/content`.
- Use Google Drive only for persistence, backups, archive packs, and restore packs.
- Commit only cleaned notebook source files after review.
- Do not commit generated data, archives, restore packs, local app workspaces, notebook outputs, or runtime folders.
- Keep the repository source-only.
- Use native app CLI commands whenever available.
- Notebook code should orchestrate, validate, parse, display, and review outputs.
- Notebook code should not reimplement native Fintech ingestion, StratLake feature generation, archive/restore, strategy, backtest, or artifact logic.

## Recommended Staging Folder Layout

Use a local or Google Drive staging folder outside the Git repository:

```text
notebook_import_staging/
|-- ready_for_review/
|-- needs_cleanup/
|-- needs_rewrite/
|-- upstream_triage_needed/
`-- do_not_import/
```

This layout is for local or Google Drive staging only. It must not be committed, and no staging folder should appear in `git status`.

## Readiness Categories

`ready_for_review/`

Notebook appears close to importable after cleanup and can proceed to final validation.

`needs_cleanup/`

Notebook is conceptually useful but still has outputs, execution counts, stale paths, old cells, excessive logs, or minor source cleanup needs.

`needs_rewrite/`

Notebook has useful intent but should be rewritten or heavily refactored before import because it is too runtime-specific, too stale, too duplicated, or too far from the repository standards.

`upstream_triage_needed/`

Notebook reveals behavior that may belong in `fintech-market-ingestion` or `stratlake-trade-engine`, such as native command failures, strategy failures, archive/restore issues, feature-generation issues, or data/contract handling issues.

`do_not_import/`

Notebook should not enter the repository because it is obsolete, unsafe, redundant, exploratory scratch work, or contains content that cannot be safely cleaned.

## Staging Workflow

1. Copy the notebook from Google Drive into the staging area.
2. Classify it into one readiness category.
3. Apply the notebook cleanup workflow when available.
4. Check against the secret-safe import checklist.
5. Check against notebook standards.
6. Confirm path/session conventions.
7. Confirm native-command-first behavior.
8. Run validation scripts locally.
9. Move only cleaned, reviewed notebooks into `notebooks/`.
10. Leave rejected or unresolved notebooks outside the repository.

## Per-Notebook Review Questions

- Does the notebook fit the planned Notebook 00-09 sequence?
- Does it have a stable numbered filename?
- Does it include required header metadata?
- Are outputs cleared?
- Are execution counts reset or removed where practical?
- Are there runtime dumps, private local paths, or large embedded outputs?
- Does it use `/content` for active Colab work?
- Is Google Drive limited to persistence, backup, archive, and restore use?
- Does it use native Fintech and StratLake CLI commands where available?
- Does it reimplement any upstream app logic?
- Does it depend on generated data that is not documented as a runtime artifact?
- Does it expose a failure that should be triaged upstream?

## Classification Rules

- If mostly clean and aligned with standards, classify it as `ready_for_review/`.
- If useful but containing outputs, execution counts, stale paths, stale cells, or minor cleanup needs, classify it as `needs_cleanup/`.
- If conceptually useful but structurally poor, duplicated, stale, or too runtime-specific, classify it as `needs_rewrite/`.
- If the failure appears app-side, classify it as `upstream_triage_needed/`.
- If obsolete, unsafe, redundant, or scratch-only, classify it as `do_not_import/`.

## Movement Into the Repository

- Only move notebooks into `notebooks/` after cleanup and review.
- The first Milestone 2 import should be only `00_setup_and_storage_overview.ipynb`.
- Do not bulk import Notebook 01 through Notebook 09 in this issue.
- Use the repository validation scripts before committing.
- Review the Git diff manually before commit.
- Confirm no staging folders are staged.
- Confirm no generated data, archives, restore packs, local app workspaces, runtime folders, notebook outputs, or secrets are staged.

## Validation Commands

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
```

These scripts are guardrails, not a replacement for manual review.

## Relationship to Other Milestone 1 and 2 Docs

Use this guide with:

- [Secret-Safe Notebook Import Checklist](notebook_import_checklist.md)
- [Notebook Naming, Metadata, and Commit Standards](notebook_standards.md)

Later Milestone 2 issues will add or use:

- `docs/notebook_cleanup_workflow.md`
- Reusable notebook header template.
- Notebook 00 pilot import.
- Notebook 00 audit record.
- Notebook index/import status tracker.

## Non-Goals

- Do not import Notebook 00 through Notebook 09.
- Do not add generated data.
- Do not add archive packs or restore packs.
- Do not add local app workspaces.
- Do not add CI workflows.
- Do not implement upstream app fixes.
- Do not create the notebook cleanup workflow here; that belongs to M2.2.
- Do not create the reusable notebook header template here; that belongs to M2.3.
- Do not create the notebook index here; that belongs to M2.6.

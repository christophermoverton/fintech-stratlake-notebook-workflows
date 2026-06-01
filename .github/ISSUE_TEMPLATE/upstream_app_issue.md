---
name: Upstream app issue
about: Capture failures that may belong in fintech-market-ingestion or stratlake-trade-engine
title: "Upstream Triage - "
labels: upstream-triage
assignees: ""
---

## Description

Describe the failure or behavior that may belong to an upstream app repository.

## Suspected Target Repository

- [ ] `fintech-market-ingestion`
- [ ] `stratlake-trade-engine`
- [ ] Unsure / needs triage

## Notebook Reproduction Context

- Notebook:
- Session ID:
- Archive ID:
- Input data or feature source:
- Colab runtime notes:

## Native Command

Paste the native command used to reproduce the issue, with secrets and private paths removed.

```bash

```

## Observed Result

Describe what happened.

## Expected Result

Describe what should have happened.

## Evidence

- Relevant sanitized logs:
- Error summary:
- Artifact or report path, if safe to share:
- Screenshots, if safe and free of secrets:

## Why This Appears Upstream

Explain why the failure appears to involve native app behavior rather than notebook orchestration.

## Notebook Repo Boundary

This notebook repository should preserve reproduction context and summarize failures. If the fix requires changing native ingestion, archive/restore, feature generation, strategy, backtest, diagnostic, or artifact logic, the implementation should move to the appropriate upstream app repository.

## Notebook 09 Strategy Triage, if applicable

- Strategy/config that succeeded:
- Strategy/configs that failed:
- Shared input data/session:
- Command used:
- Failure summary:
- Likely notebook-prep issue?
- Likely app-side strategy/config/diagnostic issue?

## Acceptance Criteria

- [ ] Reproduction context is documented without secrets or generated data.
- [ ] Native command and sanitized evidence are included.
- [ ] Target repository is identified or marked for triage.
- [ ] Notebook workflow changes, if any, are limited to orchestration, validation, parsing, display, or review.
- [ ] Upstream implementation work is tracked in the appropriate app repository when needed.

## Validation

List validation commands, reruns, or checks used to confirm the failure and its likely owner.

## Notes

Add links to upstream issues, notebook audit issues, or related strategy comparison notes.

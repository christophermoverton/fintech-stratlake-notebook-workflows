---
name: Milestone task
about: Track implementation work for a project milestone
title: "M1.x - "
labels: milestone-1
assignees: ""
---

## Description

Describe the milestone task and why it is needed.

## Context

- Milestone:
- Related issue or dependency:
- Repository area:
- Upstream apps involved, if any:

## Deliverables

- [ ] Deliverable 1
- [ ] Deliverable 2
- [ ] Documentation updated, if applicable

## Acceptance Criteria

- [ ] Scope is clear and limited to this repository.
- [ ] Deliverables are complete.
- [ ] Generated data, secrets, notebook outputs, archive packs, restore packs, and local workspaces are not added unless explicitly intended and safe.
- [ ] Native-command-first repository boundary is preserved.
- [ ] Manual review and validation are complete.

## Validation

List the validation commands or checks for this task.

```bash
python scripts/scan_for_secret_patterns.py .
python scripts/check_notebooks_no_outputs.py notebooks
python scripts/validate_repo_cleanliness.py .
```

## Non-Goals

- Do not import notebooks unless this task explicitly covers reviewed notebook import.
- Do not add generated data, archives, restore packs, local app workspaces, notebook outputs, or secrets.
- Do not implement upstream app fixes in this repository.
- Do not add GitHub Actions workflows unless explicitly scoped.

## Notes

Add implementation notes, review notes, or follow-up tasks.

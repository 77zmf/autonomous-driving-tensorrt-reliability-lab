# Contributing Guide

This documentation is now maintained in the reliability lab. Follow the
[lab contribution guide](../../CONTRIBUTING.md), keep the imported MIT notice,
and record significant changes in [the changelog](CHANGELOG.md). The original
source-repository conventions below are retained as documentation context.

Thank you for contributing to this SOP repository.

This repository documents **release and version governance practices**.
Clarity and traceability are the top priorities.

---

## Commit Message Convention

Use the following prefixes:

- `docs:` documentation content changes
- `diagram:` flowchart or visualization updates
- `template:` template updates
- `chore:` structure, rename, or non-content changes

Examples:
- `docs: add rollback procedure`
- `diagram: update release flow`
- `template: extend test report fields`

---

## Branching Model

- `main`: stable, published documentation
- `draft/*`: major edits or restructuring
- `hotfix/*`: urgent fixes

All published documentation must be merged into `main`.

---

## Writing Style

- Be explicit and concise
- Prefer checklists and steps over long paragraphs
- Avoid company-specific or confidential information

---

## Diagrams

- Use Mermaid for flow diagrams
- Ensure diagrams render correctly in both GitHub and Typora

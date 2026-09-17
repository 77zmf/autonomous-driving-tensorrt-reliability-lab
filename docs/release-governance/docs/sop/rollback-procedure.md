# Rollback & Incident Response Procedure

## 1. Purpose

Define a clear and safe rollback procedure when a released version
causes functional, performance, or safety issues.

---

## 2. Core Principles

- Never modify historical tags
- Rollback is performed by switching to a previous tag
- Fixes must go through a new release cycle

---

## 3. Rollback Scenarios

### Scenario A: Issue found before stable release
- Do NOT create Release tag
- Return to test branch
- Fix and re-test

### Scenario B: Issue found after Release
- Identify last known good tag
- Roll back deployment to that tag
- Start hotfix process

---

## 4. Rollback Procedure

### Step 1: Identify last stable version
```bash
git tag --list
git checkout v0.46.0.20260101.Release

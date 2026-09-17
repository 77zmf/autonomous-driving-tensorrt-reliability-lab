# Autoware Version Release SOP

## 1. Purpose

This document defines the **standard release process** for Autoware-based projects,
ensuring that each released version is:

- Traceable
- Reproducible
- Test-verified
- Safe to deploy

---

## 2. Scope

- **Release repository**: `autoware`
- **Dependency repositories** (not directly released):
  - autoware_universe
  - autoware_launch
  - autoware_msgs
  - other dependent repositories

> Only the `autoware` repository is allowed to publish release tags.

---

## 3. Roles & Responsibilities

### Test Owner
- Conduct functional, simulation, and vehicle tests
- Provide clear test results and conclusions

### Release Owner
- Manage release branches
- Lock dependency versions
- Merge into main branch
- Create and publish release tags

> One person may assume both roles.

---

## 4. Version Naming Convention

### Beta Version

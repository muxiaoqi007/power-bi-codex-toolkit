# Plugin Foundation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn the repository into a validated, installable Codex plugin that can grow to contain multiple Power BI Skills.

**Architecture:** Treat the repository root as one Codex plugin and discover Skills from `./skills/`. Add a repository-owned validator and tests so GitHub Actions can verify the plugin without relying on a developer's global Codex installation.

**Tech Stack:** Codex plugin JSON, Codex Skills, Python 3.11, PyYAML, unittest, GitHub Actions.

---

### Task 1: Add the plugin manifest

**Files:**
- Create: `.codex-plugin/plugin.json`

1. Start from the official `plugin-creator` scaffold.
2. Replace scaffold metadata with the public repository identity.
3. Point `skills` at `./skills/`.
4. Run the official plugin validator and fix all failures.

### Task 2: Add repository validation

**Files:**
- Create: `scripts/validate_repository.py`
- Create: `requirements-dev.txt`

1. Validate the plugin manifest and semantic version.
2. Discover every Skill directory and validate frontmatter, folder naming, UI metadata, JSON assets, and Python scripts.
3. Return a non-zero status for any violation.
4. Run the validator and confirm it passes.

### Task 3: Test deterministic layout checks

**Files:**
- Create: `tests/test_layout_validator.py`
- Create: `tests/fixtures/layout-valid.json`
- Create: `tests/fixtures/layout-invalid.json`

1. Add a passing fixture.
2. Add overlap and out-of-bounds failures.
3. Run `python -m unittest discover -s tests -v` and confirm all tests pass.

### Task 4: Add continuous integration

**Files:**
- Create: `.github/workflows/validate.yml`

1. Install Python and development dependencies.
2. Run repository validation.
3. Run unit tests.
4. Confirm the workflow YAML parses and push it to GitHub.

### Task 5: Document contribution and installation

**Files:**
- Modify: `README.md`
- Create: `CONTRIBUTING.md`

1. Explain the plugin architecture and direct Skill installation.
2. Document how to add and validate a new Skill.
3. Update the roadmap and verification commands.
4. Commit and push the completed foundation.

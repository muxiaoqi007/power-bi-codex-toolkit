# PBIR Inspection Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a read-only Codex Skill and deterministic static inspector for PBIR project structure and page layouts.

**Architecture:** Keep procedural guidance in the Skill and implement zero-dependency file checks in Python. Validate only locally provable structure and layout; route full schema, semantic-model, and rendering checks to their canonical tools.

**Tech Stack:** Codex Skills, Python 3.11, PBIR JSON, unittest.

---

### Task 1: Create the inspection Skill

- Scaffold `skills/inspect-pbir-report/` with the official Skill initializer.
- Define diagnostic triggers, read-only workflow, scope, and safety boundaries.
- Add PBIR structure and inspection-output references.

### Task 2: Implement static inspection

- Discover `.Report` directories from project, `.pbip`, and report paths.
- Check JSON syntax, required files and fields, bindings, identifiers, page ordering, visual positions, bounds, and overlap.
- Support text and JSON output with deterministic exit codes.

### Task 3: Add automated tests

- Test a clean minimal report.
- Test overlap warnings.
- Test missing page errors.
- Test out-of-bounds visual errors.

### Task 4: Integrate and release

- Validate the Skill and plugin.
- Update README and plugin metadata.
- Install the Skill globally, push, run CI, and publish version 0.3.0.

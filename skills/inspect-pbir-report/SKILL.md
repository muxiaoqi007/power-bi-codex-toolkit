---
name: inspect-pbir-report
description: Inspect and diagnose Power BI Enhanced Report (PBIR) projects without modifying them. Use when a user asks to validate a .pbip project, inspect a .Report folder, diagnose why a PBIR report or page will not open or render, find missing pages or visuals, detect invalid JSON, check page order and active page references, audit visual positions for overlap or bounds, or obtain a structural inventory before editing.
---

# Inspect PBIR Report

Inspect first and keep diagnosis separate from repair. Prefer deterministic checks, report tool limitations explicitly, and never rename PBIR folders automatically because identifiers cascade through multiple files.

## Workflow

1. Identify the target: `.pbip` file, project directory, or `.Report` directory. If the input is `.pbix`, explain that it must be saved as PBIP/PBIR before file-level inspection.
2. Run `python3 scripts/inspect_pbir.py <path>`. Add `--json` when machine-readable findings are useful.
3. Read `references/pbir-structure.md` only when interpreting folder relationships, bindings, or identifiers.
4. Classify findings:
   - Errors: malformed or missing required files/fields, broken page references, invalid identifiers, invalid dimensions, or out-of-bounds visuals.
   - Warnings: orphan folders, overlaps, stale active pages, folder-name portability risks, or objects that require rendered review.
5. If `pbir` CLI exists, recommend or run `pbir validate <Report.Report> --all` for full Microsoft schema, semantic-model field, role, and catalog validation. Do not claim the static inspector replaces it.
6. Use `references/review-output.md` to report scope, inventory, findings, evidence, and unverified areas.
7. When asked only to inspect or diagnose, do not mutate files. When asked to fix, propose the exact cascade and validate after every change.

## Safety Rules

- Never rename page, visual, bookmark, or report folders as an automatic fix.
- Never invent a missing semantic-model binding or connection string.
- Do not treat syntactically valid JSON as proof that a visual renders.
- Treat overlap findings as warnings because intentional layering and groups exist.
- Do not expose connection strings in summaries; report only the binding type and whether required values exist.
- Preserve unsupported or newer schema content unless the user explicitly asks for migration.

## Static Inspector Coverage

The bundled inspector checks:

- Target discovery and `.Report` folder presence.
- JSON syntax and expected schema URL prefix.
- `definition.pbir` version and dataset-reference shape.
- Required report, page-list, page, and visual files/fields.
- Page order, active page, missing page folders, and orphan page folders.
- Page/visual identifier format, including readable folders whose JSON declares opaque identifiers.
- Page dimensions and visual position dimensions.
- Visual bounds and pairwise overlap warnings.

It does not validate model field references, visual data roles, all schema enums, custom-visual packages, DAX, rendering, bookmarks, or Fabric availability.

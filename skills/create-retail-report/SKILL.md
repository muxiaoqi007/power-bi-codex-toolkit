---
name: create-retail-report
description: Design, create, redesign, or review decision-focused retail Power BI report frontends. Use for retail dashboards, store or regional performance pages, sales and margin analysis, product/category performance, inventory health, KPI selection, page architecture, visual layout, PBIR implementation plans, and quality reviews of Power BI report pages.
---

# Create Retail Report

Turn retail business questions and a semantic model into a concise Power BI report design. Keep business intent, visual design, and PBIR implementation separate until the design brief is approved.

## Workflow

1. Inspect the available model, PBIP/PBIR files, measures, dimensions, and delivery constraints. Do not invent fields that have not been confirmed.
2. Resolve missing context: audience, business cadence, comparison baseline, store hierarchy, currency, page size, and delivery surface.
3. Draft one design brief using `references/design-brief.md`. Give every page one job and trace every visual to a decision question.
4. Select KPIs from `references/retail-kpis.md`. Prefer existing governed measures. Mark proposed measures explicitly.
5. Map each page intent to a pattern from `references/page-patterns.md`. Derive coordinates from page dimensions, margins, and gaps; never place by eye.
6. Present the brief and obtain approval before modifying PBIR files or generating a report.
7. Implement with the tools available in the environment. Prefer theme-level styling over repeated visual overrides. Copy `assets/retail-theme.json` only when a neutral starter theme is useful and the user has not supplied a brand theme.
8. After each structural mutation, run the project's native validator. For a layout-spec JSON file, also run `python3 scripts/validate_layout.py <layout.json>`.
9. Review the result against `references/quality-gate.md`. Distinguish file-level validation from visual inspection; do not claim visual quality without rendering or opening the report.

## Design Rules

- Optimize for decisions, not chart count.
- Use one primary message per page and normally 5-8 visible analytical objects.
- Put summary first, explanation second, detail last.
- Reserve the accent color for focus or selection; use semantic colors only for meaning.
- Show comparison context on every headline KPI: target, prior period, prior year, or another approved baseline.
- Prefer direct labels and meaningful titles over legends and generic names.
- Keep filters purposeful. Use the filter pane for secondary controls and visible slicers for frequent decisions.
- Preserve accessible contrast and never encode status by color alone.
- Do not allow visual overlap or out-of-bounds placement.

## Output Contract

Return or save these artifacts as appropriate:

1. Approved design brief.
2. Page inventory with each page's job and decision questions.
3. Visual inventory with measure, dimension, comparison, interaction, and placement.
4. Assumptions and missing semantic-model objects.
5. Validation results and remaining visual checks.

When the user asks only for review, do not mutate files. When the user asks to build, implement and validate the report rather than stopping at recommendations.

## Resource Routing

- Read `references/design-brief.md` when planning or changing report scope.
- Read `references/retail-kpis.md` when choosing or defining measures.
- Read `references/page-patterns.md` when deciding page composition or coordinates.
- Read `references/quality-gate.md` before presenting a design or completed build.
- Run `scripts/validate_layout.py` when a layout specification is available.
- Use `assets/retail-theme.json` as a starter, not as a replacement for an existing brand system.

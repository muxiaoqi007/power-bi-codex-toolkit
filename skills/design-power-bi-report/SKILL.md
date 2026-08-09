---
name: design-power-bi-report
description: Design new Power BI report frontends or redesign existing ones from business questions and semantic-model fields. Use for report architecture, page planning, KPI selection, chart selection, layout grids, interaction design, design systems, themes, executive dashboards, analytical reports, operational monitoring, and PBIR implementation specifications across any industry.
---

# Design Power BI Report

Convert decision questions and confirmed semantic-model objects into an approved, implementation-ready Power BI report design. Do not begin with charts; begin with decisions.

## Workflow

1. Inspect provided requirements, model metadata, PBIP/PBIR files, screenshots, themes, and delivery constraints. Separate confirmed facts from assumptions.
2. Complete the design contract in `references/design-contract.md`: audience, purpose, cadence, decision questions, scope, delivery surface, and data contract.
3. Give each page one job. Map every planned visual to at least one approved decision question; remove visuals without a decision role.
4. Select visual forms using `references/chart-selection.md`. Prefer the simplest form that exposes comparison, change, distribution, relationship, flow, or detail.
5. Commit one design system using `references/design-system.md`: hierarchy, typography, spacing, color roles, titles, cards, tables, and accessibility.
6. Define layout rows in JSON and run `python3 scripts/generate_grid.py <grid.json> --output <layout.json>`. Check the generated layout with the available overlap/bounds validator.
7. Specify every visual's title, purpose, measure, dimension, comparison, sort, interaction, tooltip, and rectangle before PBIR implementation.
8. Present the design contract, page inventory, and layout for approval. Treat approval as a lock; reopen it explicitly when scope changes.
9. If the user asked only for design, stop at the approved specification. If the user asked to build, implement with available PBIR tools and validate after each structural mutation.

## Non-Negotiable Rules

- Never invent model fields without labeling them as proposed.
- Show a target, prior period, prior year, or approved peer comparison on headline KPIs.
- Keep normal analytical pages to roughly 5-8 visible objects unless an operational density requirement justifies more.
- Derive positions arithmetically; do not place visuals by eye.
- Prefer theme-level formatting over repeated visual overrides.
- Reserve accent color for focus; reserve semantic colors for meaning.
- Do not encode status by color alone.
- Distinguish structural validation from rendered visual review.

## Output Contract

Produce:

1. Design contract with explicit assumptions.
2. Page inventory: page name, one job, decision questions, and audience action.
3. Visual specification: title, purpose, fields, comparison, sort, interaction, and rectangle.
4. Design-system tokens and theme decision.
5. Missing or proposed semantic-model objects.
6. Validation evidence and remaining rendered-page checks.

## Resource Routing

- Read `references/design-contract.md` during discovery and whenever scope changes.
- Read `references/chart-selection.md` before choosing visual types.
- Read `references/design-system.md` before setting layout, color, typography, or component styling.
- Run `scripts/generate_grid.py` to turn row/column intentions into exact rectangles.
- Use `assets/power-bi-neutral-theme.json` only as an unbranded starting point.

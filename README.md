# Create Retail Report for Codex

A Codex Skill for designing, building, redesigning, and reviewing decision-focused retail Power BI report frontends.

It turns business questions into an approved design brief, selects governed retail KPIs, maps each page to a purposeful layout, and applies structural and visual quality gates before delivery.

## What it covers

- Executive retail dashboards
- Store and regional performance
- Sales, growth, and margin analysis
- Product and category performance
- Inventory health
- Page architecture and visual layout
- Power BI/PBIR implementation planning
- Accessibility and design review

## Repository structure

```text
skills/create-retail-report/
├── SKILL.md
├── agents/openai.yaml
├── assets/retail-theme.json
├── references/
│   ├── design-brief.md
│   ├── page-patterns.md
│   ├── quality-gate.md
│   └── retail-kpis.md
└── scripts/validate_layout.py
```

`SKILL.md` contains the main workflow. Detailed domain knowledge is loaded progressively from `references/`, deterministic layout checks live in `scripts/`, and reusable report styling lives in `assets/`.

## Install

Clone the repository and copy the Skill into the Codex skills directory:

```bash
git clone https://github.com/YOUR-USER/codex-retail-report.git
mkdir -p ~/.codex/skills
cp -R codex-retail-report/skills/create-retail-report ~/.codex/skills/
```

Restart Codex after installation so the Skill is discovered.

## Use

Invoke it explicitly:

```text
$create-retail-report Design an executive retail dashboard for weekly trading performance.
```

Additional examples:

```text
$create-retail-report Create a store-performance report that highlights regional outliers.

$create-retail-report Review this PBIR report for layout, KPI context, interaction, and accessibility issues.

$create-retail-report Design an inventory-health page for stockout, overstock, and aged-stock decisions.
```

The Skill can also trigger implicitly for relevant retail Power BI report requests.

## Layout validation

The included zero-dependency validator checks a simple layout specification for invalid sizes, duplicate names, out-of-bounds visuals, and overlap:

```bash
python3 skills/create-retail-report/scripts/validate_layout.py layout.json
```

Example input:

```json
{
  "page": {"width": 1280, "height": 720},
  "visuals": [
    {"name": "page-title", "x": 24, "y": 20, "width": 1232, "height": 64},
    {"name": "net-sales", "x": 24, "y": 104, "width": 296, "height": 112}
  ]
}
```

This validator supplements rather than replaces native PBIR/PBIP validation and rendered-page inspection.

## Validate the Skill

If the Codex `skill-creator` utilities are installed:

```bash
uv run --with pyyaml python \
  ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/create-retail-report
```

## Design principles

- Optimize for decisions, not chart count.
- Give every page one primary job.
- Trace every visual to an approved decision question.
- Keep business intent, visual design, and PBIR implementation separate until approval.
- Prefer theme-level styling over repeated visual overrides.
- Report structural validation and visual inspection separately.

## License

MIT License. See [LICENSE](LICENSE).

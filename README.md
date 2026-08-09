# Power BI Codex Toolkit

An extensible collection of Codex Skills, references, assets, and validation tools for agentic Power BI report development.

The toolkit currently includes general report design, retail-specialized design, and static PBIR inspection. It turns business questions into approved designs and checks report files before deeper schema or rendered validation.

The repository is intended to grow into a broader toolkit covering report design, industry-specific reporting workflows, PBIR authoring and validation, themes, reusable page patterns, and custom visuals.

It is packaged as a Codex plugin: the root `.codex-plugin/plugin.json` discovers every Skill under `skills/`.

## Current capabilities

- General Power BI report architecture and page design
- Deterministic 12-column page-grid generation
- Chart selection and reusable report design-system guidance
- Read-only PBIR structure and page-layout inspection
- Page-order, identifier, visual bounds, and overlap diagnostics
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
.codex-plugin/plugin.json
skills/design-power-bi-report/
├── SKILL.md
├── agents/openai.yaml
├── assets/power-bi-neutral-theme.json
├── references/
│   ├── chart-selection.md
│   ├── design-contract.md
│   └── design-system.md
└── scripts/generate_grid.py
skills/inspect-pbir-report/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── pbir-structure.md
│   └── review-output.md
└── scripts/inspect_pbir.py
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

Additional Skills can be added under `skills/` without changing the installation model.

## Install

Clone the repository and copy the Skill into the Codex skills directory:

```bash
git clone https://github.com/muxiaoqi007/power-bi-codex-toolkit.git
mkdir -p ~/.codex/skills
cp -R power-bi-codex-toolkit/skills/* ~/.codex/skills/
```

Restart Codex after installation so the Skill is discovered.

The repository can also be consumed as a Codex plugin by environments that support installation from a Git repository. The plugin manifest discovers all current and future Skills under `skills/`.

## Use

Invoke it explicitly:

```text
$design-power-bi-report Turn my business questions and semantic model into a Power BI report design.

$inspect-pbir-report Inspect this PBIR project for structural and layout problems.

$create-retail-report Design an executive retail dashboard for weekly trading performance.
```

Additional examples:

```text
$create-retail-report Create a store-performance report that highlights regional outliers.

$create-retail-report Review this PBIR report for layout, KPI context, interaction, and accessibility issues.

$create-retail-report Design an inventory-health page for stockout, overstock, and aged-stock decisions.
```

The Skills can also trigger implicitly for relevant Power BI report requests.

## Generate a page grid

The general design Skill includes a deterministic 12-column grid generator. Define rows and column spans, then generate exact visual rectangles:

```bash
python3 skills/design-power-bi-report/scripts/generate_grid.py \
  tests/fixtures/grid-spec.json \
  --output layout.json
```

The resulting layout can be checked with the retail layout validator or adapted into PBIR visual positions.

## Inspect a PBIR project

Run the zero-dependency, read-only static inspector on a project directory, `.pbip` file, or `.Report` folder:

```bash
python3 skills/inspect-pbir-report/scripts/inspect_pbir.py path/to/project
python3 skills/inspect-pbir-report/scripts/inspect_pbir.py path/to/project --json
```

The inspector checks local structure, JSON syntax, page references, identifiers, visual bounds, and overlap. It does not replace `pbir validate --all` or rendered-page inspection.

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

Validate the whole repository before contributing:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_repository.py
python -m unittest discover -s tests -v
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

## Roadmap

- Deeper PBIR schema and field-reference validation
- Reusable executive, store, inventory, and product page patterns
- Industry-specific reporting Skills beyond retail
- Custom visual and theme tooling

Contributions are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).

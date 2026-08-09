# Contributing

Contributions should keep the toolkit focused on Power BI report development and preserve progressive disclosure: concise Skill workflows, detailed references, deterministic scripts, and reusable assets.

## Add a Skill

1. Create `skills/<skill-name>/` using lower-case hyphen-case.
2. Add `SKILL.md` with only `name` and `description` in YAML frontmatter.
3. Put detailed domain knowledge in `references/`, repeated deterministic operations in `scripts/`, and reusable output material in `assets/`.
4. Add `agents/openai.yaml` with a default prompt that explicitly mentions `$<skill-name>`.
5. Add focused tests for scripts and fragile workflows.
6. Run the complete validation suite before opening a pull request.

## Validate

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_repository.py
python -m unittest discover -s tests -v
```

When the Codex `plugin-creator` and `skill-creator` utilities are available, also run their official validators against the plugin root and changed Skill.

## Pull requests

Explain the user request that should trigger the Skill, the reusable knowledge or automation added, and how the change was tested. Do not include credentials, proprietary data, customer report files, or unlicensed brand assets.

# PBIR Structure Mental Model

```text
Project.pbip
Report.Report/
├── definition.pbir
└── definition/
    ├── version.json
    ├── report.json
    └── pages/
        ├── pages.json
        └── <page-id>/
            ├── page.json
            └── visuals/
                └── <visual-id>/visual.json
```

## Identifier relationships

- `pages.json.pageOrder[]` contains page identifiers, not display names.
- `pages.json.activePageName` should be one of the identifiers in `pageOrder`.
- `page.json.name` matches the page identifier. The containing folder may instead use a readable name.
- `visual.json.name` is the visual identifier. The containing folder may instead use a readable name.
- Display names are user-facing labels and may contain spaces; identifiers are machine-facing.

Folder names and identifiers are distinct concepts. Renaming an identifier requires a reference cascade; never assume a folder-only rename changes the report object identity.

## Dataset binding

`definition.pbir.datasetReference` uses one of:

- `byPath.path`: a local semantic-model directory, resolved relative to the `.Report` folder.
- `byConnection.connectionString`: a service connection for a thin report.

Static inspection verifies shape and local path existence. It does not authenticate a service connection.

## Validation layers

1. JSON syntax.
2. Required files and structural relationships.
3. Microsoft JSON schema and version compatibility.
4. Semantic model fields, roles, and visual catalog.
5. Rendered output and interaction behavior.

The bundled inspector covers layers 1-2 plus layout heuristics. Use `pbir validate --all` and rendered inspection for the remaining layers.

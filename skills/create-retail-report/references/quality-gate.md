# Retail Report Quality Gate

## Business

- Every page has one stated job.
- Every visual answers an approved decision question.
- KPI definitions, comparisons, time grain, currency, and scope are explicit.
- Proposed measures are distinguished from confirmed model objects.

## Information Design

- The first scan reveals status, magnitude, and exception.
- Titles state the subject or finding instead of chart type.
- Chart choice matches the analytical question.
- Detail is available without competing with the overview.
- Accent and semantic colors have consistent meanings.

## Interaction

- Slicers represent frequent decisions; secondary filters stay in the filter pane.
- Cross-filter behavior is intentional and reset behavior is clear.
- Navigation and drill paths have visible labels.
- Tooltips add context rather than repeat labels.

## Accessibility

- Text and key marks have sufficient contrast.
- Status is not encoded by color alone.
- Reading and tab order follow the visual hierarchy.
- Titles and alternative text describe the analytical meaning.

## Structural Validation

- No overlap or out-of-bounds visuals.
- Names, bindings, measures, and theme references resolve.
- Native PBIR/PBIP validation passes after mutations.
- Rendered pages are visually inspected at the intended consumption size.

Report file validation and visual inspection separately. A structurally valid report can still be poorly designed.

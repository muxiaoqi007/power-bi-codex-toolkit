# Retail Report Design Brief

Complete this brief before implementation. Mark uncertain statements as assumptions.

```yaml
audience: role, decisions, and expected analytical fluency
purpose: one outcome the report exists to drive
cadence: daily | weekly | monthly | quarterly
delivery:
  surface: Power BI Service | embedded | Desktop | mobile
  page_size: width x height
  mobile_required: true | false
scope:
  date_range:
  geography:
  channels:
decision_questions:
  - concrete question answerable from the report
pages:
  - name:
    job: one sentence; exactly one job
    serves: [decision question]
    primary_measure:
design_identity:
  tone: quiet analytical | high-contrast executive | operational dense
  accent_rule:
  comparison_style:
  title_style:
  spacing: margin and gap values
data_contract:
  confirmed_measures: []
  confirmed_dimensions: []
  proposed_measures: []
  unresolved: []
```

## Approval Gate

Ask for approval of the assembled brief, not a second discovery interview. After approval, treat it as frozen. If scope changes, amend and reconfirm the affected fields before rebuilding visuals.

Reject visuals that do not answer a listed decision question. Reject pages that duplicate another page's job.

# Power BI Design Contract

Complete and approve this contract before implementation. Mark guesses as assumptions and unconfirmed fields as proposed.

```yaml
audience:
  role:
  decisions:
  analytical_fluency:
purpose: one outcome the report exists to drive
cadence: realtime | daily | weekly | monthly | quarterly
decision_questions:
  - a concrete question the viewer must answer
scope:
  time:
  organization:
  geography:
  exclusions: []
delivery:
  surface: Power BI Service | embedded | Desktop | mobile
  page_size: width x height
  mobile_required: true | false
pages:
  - name:
    job: exactly one job
    serves: [decision question]
    action: what the viewer does after reading it
data_contract:
  confirmed_measures: []
  confirmed_dimensions: []
  proposed_objects: []
  unresolved: []
```

## Approval

Present the completed contract once. Approval freezes audience, scope, page jobs, decision questions, and delivery constraints. Later changes reopen only the affected fields and require reconfirmation before rebuilding visuals.

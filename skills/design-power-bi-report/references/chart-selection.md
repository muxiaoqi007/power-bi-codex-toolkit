# Chart Selection

Choose the visual from the analytical relationship, not from decoration preferences.

| Question | Default visual | Use when | Avoid when |
|---|---|---|---|
| What is the current status? | KPI/card with comparison | one governed headline measure matters | there is no baseline or target |
| How did it change? | line chart | time is continuous and trend matters | categories are unordered |
| Which categories lead or lag? | sorted horizontal bar | ranking and label readability matter | there are too many low-value categories |
| How does composition differ? | stacked bar or 100% stacked bar | both total and mix, or mix alone, matter | precise segment comparison is required across many groups |
| What is the distribution? | histogram, box plot, or binned column | spread and outliers drive decisions | only an aggregate is available |
| Are two measures related? | scatterplot | correlation, clusters, and outliers matter | there are too few observations |
| Where is the exception? | conditional-format matrix or ranked bar | users must locate a specific entity | the table is included only as a data dump |
| Where is it geographically? | map | spatial position or distance changes the decision | geography is merely another category |
| How does a process flow? | funnel or flow visual | ordered stage loss or movement matters | stages are not mutually comparable |

## Selection Tests

- Prefer position and length over angle and area for precise comparisons.
- Use direct labels when they remove legend lookup.
- Sort categorical charts by the decision variable unless sequence has inherent meaning.
- Do not use gauges when a compact KPI with target variance communicates more information.
- Use custom visuals only when core visuals cannot express the required analytical relationship.

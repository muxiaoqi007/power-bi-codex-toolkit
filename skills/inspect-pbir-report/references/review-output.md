# Inspection Output

Use this structure so conclusions remain attributable to the check that produced them.

```text
PBIR inspection
- Target:
- Reports discovered:
- Pages / visuals inspected:
- Static inspector: pass | warnings | errors
- pbir CLI: passed | failed | unavailable | not run
- Rendered inspection: completed | not completed

Errors
1. [code] path — evidence and impact

Warnings
1. [code] path — evidence and why manual judgment is needed

Unverified
- model field references
- visual roles and catalog properties
- rendering and interaction behavior
```

Lead with blocking errors. Keep warnings separate. Do not say “valid Power BI report” when only static checks ran; say “passed the bundled static checks.”

# Retail KPI Selection

Use governed measures already present in the semantic model. The formulas below describe intent; they are not permission to invent schema names.

| Decision | Headline KPI | Required context | Useful diagnostics |
|---|---|---|---|
| Are sales on plan? | Net sales | target and prior year variance | transactions, units, average selling price |
| Is growth healthy? | Comparable-store sales growth | store eligibility definition | traffic, conversion, basket size |
| Are we profitable? | Gross margin and margin rate | budget or prior year | markdown, discount, product mix |
| Are stores productive? | Sales per store or area | comparable cohort | labor hour, footfall, conversion |
| Is inventory healthy? | Weeks of supply or stock cover | target band | sell-through, stockout rate, aged inventory |
| Is assortment working? | Category/product sales and margin | contribution share | velocity, availability, return rate |

## Definition Guardrails

- Define net sales treatment for tax, returns, cancellations, and discounts.
- Define comparable-store eligibility and the comparison window.
- Separate value growth from price, volume, mix, and footprint effects where decisions require it.
- State whether margin is gross profit, contribution margin, or another governed definition.
- State inventory snapshot timing and whether weeks of supply uses forecast or trailing demand.
- Avoid adding every KPI to the overview. Select 3-5 that directly serve its decision questions.

## Comparison Rules

Every headline number needs one approved comparison: target, prior period, prior year, or peer cohort. Use both absolute and percentage variance only when each changes the decision. Display direction as text or icon in addition to color.

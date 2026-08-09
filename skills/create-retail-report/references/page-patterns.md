# Retail Page Patterns

Choose the smallest set of pages that answers the approved decision questions.

## Executive Overview

- Job: determine whether trading is on track and where attention is required.
- Composition: 3-5 KPI cards, one time trend, one ranked exception view, optional compact detail.
- Avoid: separate charts for every dimension and decorative gauges.

## Store and Region Performance

- Job: locate geographic outliers and distinguish scale from performance.
- Composition: ranked bar or matrix, comparison scatterplot, trend for selected region/store, hierarchy slicer.
- Use maps only when spatial position changes the decision.

## Product and Category Performance

- Job: find categories or products driving growth and margin change.
- Composition: category contribution, sales-versus-margin view, product exceptions, drillable detail matrix.

## Inventory Health

- Job: identify stockout, overstock, and aged-stock risk.
- Composition: health KPIs, target-band distribution, exception ranking, SKU/store detail.

## Layout Arithmetic

For page width `W`, height `H`, margin `M`, gap `G`, and `N` equal columns:

```text
usable_width = W - 2M
column_width = (usable_width - (N - 1)G) / N
x(i) = M + i(column_width + G)
```

Reserve a title/header band first. Place all analytical objects below it. Use a detail gradient: summary at the top, explanations in the middle, row-level evidence at the bottom.

Represent layouts for validation as:

```json
{
  "page": {"width": 1280, "height": 720},
  "visuals": [
    {"name": "page-title", "x": 24, "y": 20, "width": 1232, "height": 64},
    {"name": "net-sales", "x": 24, "y": 104, "width": 296, "height": 112}
  ]
}
```

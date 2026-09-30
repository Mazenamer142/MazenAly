# 01 | Business case and scope

> **Case-study scenario.** This uses the public Maven Analytics "Maven Toys" dataset. There is no real client: the business problem, stakeholders and objectives below are a realistic scenario written to show the business analysis process end to end.

## Background
Maven Toys is a chain of 50 toy stores across Mexican cities (29 downtown, 12 commercial, 6 residential, 3 airport). The data covers 829,262 sale lines from 1 Jan 2022 to 30 Sep 2023 across 35 products in 5 categories.

## Business problem
Sales are growing fast, but profit is not keeping pace. Comparing Jan-Sep 2023 with Jan-Sep 2022, revenue grew **30.9%** but profit only **16.0%**, and the blended margin fell from **29.5% to 26.2%**. Leadership can see revenue in a report but has no single view that shows *why* margin is moving, which products and stores drive it, or where stock is going out.

## Objectives (what a good outcome looks like)
| # | Objective | How we would know |
|---|---|---|
| O1 | Explain the margin change in terms managers can act on | A margin bridge by product is available and refreshed with each data load |
| O2 | Track profit, not just revenue, by product, category, store and location | Profit and margin sit beside revenue in every view |
| O3 | Spot stockouts and slow stock early | Stockout rate and estimated profit at risk are visible per store and product |
| O4 | Give one agreed definition of every KPI | KPI dictionary signed off by Finance and Merchandising |

*Numeric targets (for example "stockout rate below X%") are deliberately left for the stakeholders to set: the data alone cannot justify them.*

## In scope
- Sales, product, store and inventory data supplied in the dataset
- Profit, margin, growth, mix, location and inventory analysis
- A Power BI dashboard specification and data model (build handled separately)
- KPI dictionary, business rules, requirements, user stories, AS-IS / TO-BE

## Out of scope
- Pricing and promotion analysis (no price history or promotion data exists)
- Customer and basket analysis (each sale line is a single product, with no customer key)
- Forecasting and replenishment automation (proposed as a later phase)

## Assumptions
- Each product has one fixed price and one fixed cost for the whole period, so product margin does not change over time.
- Cost and price are in USD as stated in the data dictionary.
- The inventory table is a single snapshot of stock on hand, not a history.
- The last 90 days of the data (3 Jul to 30 Sep 2023) represent the current selling rate.

## Constraints and risks
| Risk | Effect | Mitigation |
|---|---|---|
| No stock history | Cannot measure past stockouts; "profit at risk" is an estimate | State the estimate method; request daily stock snapshots |
| Fixed price/cost only | Cannot separate price effects from mix effects | Document as a data request; note that today all margin movement is mix |
| 157 of 1,750 store x product pairs missing from inventory | Some stores' stock is invisible; 41 of those pairs still sell | Confirm with Operations whether the pairs are unranged or a data gap |
| Store city spelled two ways in the source | Reports would split Mexico City into two groups | Standardised in the model (BR-08) |

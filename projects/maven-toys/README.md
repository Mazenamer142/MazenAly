# Maven Toys: growth without profit

A data analysis and business analysis case study on the public **Maven Analytics "Maven Toys"** dataset (a Mexican toy-store chain: 50 stores, 35 products, 829,262 sale lines, Jan 2022 to Sep 2023).
There is no client: the business problem and stakeholders are a scenario, and are labelled that way.

## The question
Sales are growing fast. Is profit keeping up, and if not, why?

## What I found
Comparing the same nine months (Jan-Sep) of each year:

| | 2022 | 2023 | Change |
|---|---|---|---|
| Revenue | $5.32M | $6.96M | +30.9% |
| Profit | $1.57M | $1.82M | +16.0% |
| Margin | 29.5% | 26.2% | -3.3 points |

- **The margin fall is entirely a mix effect.** Each product has one fixed price and cost in the data, so blended margin can only move when the sales mix moves. The two biggest drags are **Colorbuds** (53% margin, its share of revenue fell from 17.5% to 6.3%, contribution -2.7 points) and **Magic Sand** (12.5% margin, its share rose from 0.1% to 12.5%, contribution -2.1 points).
- **Revenue rank misleads.** Lego Bricks is the largest product by revenue ($2.39M) but earns a 12.5% margin, so only 7.4% of profit. Colorbuds alone is 20.8% of all profit. The top 5 products earn 47.9% of profit.
- **Airport stores earn more per store.** 3 airport stores make about $126k profit each, versus about $77k for Downtown, Commercial and Residential. Downtown is 56% of profit only because it has 29 of the 50 stores.
- **Stockouts.** 77 of 1,593 store x product pairs (4.8%) are out of stock. The most exposed product is Playfoam (64% margin, out of stock in 13 stores). Estimated profit at risk is about $9.7k per 30 days.
- **Timing.** Friday to Sunday is 51% of revenue.

## Recommendations
1. **Investigate Colorbuds first.** Units fell 53%, which cost about $264k of profit. The data cannot say why, so check availability, supplier and competitor factors before assuming demand fell.
2. **Rank products by profit and margin, not revenue.** Review supplier terms or pricing on the 12.5%-margin volume lines (Lego Bricks, Magic Sand). Consider pairing Magic Sand with high-margin lines such as Barrel O' Slime (50%) and Etch A Sketch (48%).
3. **Restock Playfoam first**, then Action Figure and Etch A Sketch: rank restocks by profit at risk, not by count.
4. **Test more airport-type locations.** The per-store gap is large, but the dataset has no market data, so treat it as a hypothesis.
5. **Ask for better data:** daily stock history, price and cost history, promotions, and customer or basket data.

## Limitations (please read)
- Prices and costs are single fixed values, so price effects cannot be separated from mix effects.
- Inventory is a snapshot. "Profit at risk" assumes a stocked-out product keeps selling at the pair's average daily profit over the last 90 days of the data, so it is an estimate.
- 157 of the 1,750 store x product pairs are missing from the inventory table (41 of them still sell).
- No customer, basket, promotion or competitor data.

## What is in this folder
| Path | Contents |
|---|---|
| `sql/` | Six SQL scripts: clean and model, KPIs, mix, growth and margin bridge, stores and locations, inventory |
| `python/analysis.py` | Cleans the data, computes every figure in pandas, runs the SQL on the same data and **asserts the two agree**, then writes the summary files |
| `data/summary/` | Small aggregate CSVs and `site_data.json` (used by the portfolio page) |
| `docs/` | Business analysis package: scope, stakeholders, KPI dictionary, business rules, requirements and user stories, dashboard specification, AS-IS / TO-BE |

## How to run
1. Download the dataset (free) from Maven Analytics: <https://mavenanalytics.io/data-playground> ("Maven Toys Sales").
2. `pip install pandas numpy`
3. `python python/analysis.py --data "path/to/Maven Toys Data"`

The SQL is written for SQLite. Notes in the scripts show what to change for MySQL, PostgreSQL or SQL Server.

## Status
The Power BI dashboard is the centrepiece of the **business analysis** side of this project. It is being built from the specification in `docs/07_dashboard_specification.md`, and must reproduce the reconciliation table exactly. It will be linked here when published.

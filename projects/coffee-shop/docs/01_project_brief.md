# 01 | Project brief

> **Scenario.** The data is a public "Coffee Shop Sales" file. The business problem and the people are my own scenario, made up to practise the business analysis process.

## Background
The business is a small coffee shop group with 3 stores in New York (Astoria, Hell's Kitchen and Lower Manhattan). The file has 149,116 sale lines from 1 Jan to 30 Jun 2023, for 80 products.

## The problem
Sales more than doubled in six months. Average daily revenue went from **$2,635 in January to $5,550 in June**. The owner is happy, but the team is guessing when to schedule staff, when to open and close, and what to keep on the menu. Nobody has one place to look at how a normal day runs in each store.

## Objectives
| # | Objective | How we would know |
|---|---|---|
| O1 | Show how a typical day runs in each store | Revenue by hour and store is on one page |
| O2 | Help managers plan staff around the busy hours | Peak hours are flagged per store |
| O3 | Show which products carry the sales | Category, product type and size mix are visible |
| O4 | Give everybody the same definition of each number | KPI dictionary agreed with the owner |

## In scope
- The 3 stores, the sales file, all products
- Time patterns (hour, weekday, month), menu mix, store comparison
- A Power BI operations dashboard (spec here, build separate)

## Out of scope
- Profit and margin. The file has no costs, so it is revenue only.
- Customers and baskets. There is no receipt number, so I cannot tell which lines were bought together.
- Staff cost, wait times, and stock. None of that is in the data.

## Assumptions
- Each line is one product on a receipt; revenue is quantity x unit price.
- The data is complete for the 181 days (there are no missing days for any store).
- The busy months (May, June) are a mix of real growth and summer season; six months is not enough to tell them apart.

## Risks
| Risk | What it means | What I would do |
|---|---|---|
| Only 6 months of data | Cannot tell growth from season | Ask for 12 to 24 months |
| No cost data | Cannot say which products are profitable | Ask Finance for a cost per product |
| No receipt id | No basket or "goes well with" analysis | Ask the POS team if receipt numbers can be exported |
| 15 products have a second price on a few lines (1,262 lines, 0.8%) | Tiny effect on revenue | Kept each line's own price; flag to the owner |

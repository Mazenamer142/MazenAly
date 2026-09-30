# Coffee shop: three stores, three different days

A data analysis and business analysis case study on a public **Coffee Shop Sales** dataset: 3 New York stores, 80 products, 149,116 sale lines, 1 Jan to 30 Jun 2023.
There is no client. The business problem and the people are a scenario, and are labelled that way.

## The question
Sales doubled in six months. When do people buy, and what do they buy?

## What I found
- **Daily revenue doubled**, from $2,635 in January to $5,550 in June (+111%). The value of a sale line stayed at about $4.70, so the growth is more customers, not bigger orders.
- **46% of revenue is made between 7 and 11am.**
- **Same total, three different shapes.** The stores are within 3% of each other in revenue. Lower Manhattan is the most morning-heavy (51% between 7 and 11am, 8% after 5pm). Astoria opens later and has the biggest evening share (21%).
- **The weekday hardly matters.** All seven days are within 5% of each other.
- **Drinks are 77% of sales.** Only 13% of sized drinks are small.

## Limits
Six months only, no cost data (revenue, not profit), no receipt id (no basket analysis). 15 products have a second price on 1,262 lines (0.8%); I kept each line's own price.

## What is in this folder
| Folder | What |
|---|---|
| `sql/` | Six SQL scripts (SQLite): checks and clean tables, KPIs, time patterns, products, stores, growth |
| `python/analysis.py` | Repeats the analysis in pandas, runs the SQL, and stops with an error if the two disagree. Writes `data/summary/` |
| `data/summary/` | The small result tables the portfolio charts are drawn from |
| `docs/` | The business analysis package: brief, stakeholders and RACI, AS-IS / TO-BE, KPI dictionary, requirements and user stories, Power BI dashboard spec |

## Run it
```
pip install pandas numpy openpyxl
python python/analysis.py --data "path/to/Coffee Shop Sales.xlsx"
```
The raw file is a public download and is not stored in this repo (`data/raw/` is git-ignored).

## Status
The Power BI operations dashboard is the centrepiece of the business analysis side and is still to be built. When it is published, paste its link into `window.PB_EMBEDS` at the bottom of `index.html`.

AI note: I used AI to help brainstorm and to polish the writing and code in this project.

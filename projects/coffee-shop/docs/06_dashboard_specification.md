# 06 | Power BI dashboard specification

This is the build spec for the dashboard. The DAX below is a first draft and has not been tested in Power BI yet.

## Pages
| Page | Question | Visuals |
|---|---|---|
| 1. Trading | How are we doing? | KPI cards (revenue, revenue per day, units), monthly revenue per day columns, store slicer |
| 2. The day | When are we busy? | Line chart of revenue by hour with one line per store, heat map weekday x hour, busy-hours table |
| 3. The menu | What do they buy? | Category bars, product type bars, drink size donut (or bars), top 10 products |
| 4. About the data | How is it defined? | KPI dictionary, data limits, refresh notes |

## Data model
A small star schema. **fact_sales** (one row per line) connects to **dim_product** (product id), **dim_store** (store id), **dim_date** (date) and **dim_time** (hour).

## Power Query steps
1. Load the Excel file, set types (date, time, whole number, decimal).
2. Add `Revenue = qty x unit price`.
3. Add `Hour` from the time column and `Size` from the last word of the product name.
4. Build dim_product, dim_store and a date table.
5. Remove nothing: the checks found no nulls and no duplicate ids.

## Draft measures
```
Revenue = SUMX ( fact_sales, fact_sales[qty] * fact_sales[unit_price] )
Days = DISTINCTCOUNT ( dim_date[date] )
Revenue per day = DIVIDE ( [Revenue], [Days] )
Morning rush share = DIVIDE ( CALCULATE ( [Revenue], dim_time[hour] >= 7, dim_time[hour] <= 10 ), [Revenue] )
```

## Reconciliation table
The dashboard is only accepted when these match the analysis.

| Check | Expected |
|---|---|
| Sale lines | 149,116 |
| Units | 214,470 |
| Revenue | $698,812 |
| Revenue per day | $3,861 |
| Revenue, Astoria / Hell's Kitchen / Lower Manhattan | $232,244 / $236,511 / $230,057 |
| Share of revenue 7 to 10am, all stores | 45.8% |
| Coffee + Tea + Drinking Chocolate share | 77.1% |

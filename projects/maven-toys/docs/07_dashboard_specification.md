# 07 | Power BI dashboard specification and model

> Build guide for the dashboard. The DAX below is a **reference draft**: it was not executed here. Check every measure against the reconciliation table at the bottom, which comes from the SQL in `../sql` (verified against a separate pandas calculation).

## Data model (star schema)
| Table | Grain | Key columns |
|---|---|---|
| FactSales | one row per sale line (829,262) | Sale_ID, Date, Store_ID, Product_ID, Units |
| FactInventory | one row per store x product (1,593) | Store_ID, Product_ID, Stock_On_Hand |
| DimProduct | product (35) | Product_ID, Product_Name, Product_Category, Unit_Cost, Unit_Price |
| DimStore | store (50) | Store_ID, Store_Name, City, Location, Open_Date |
| DimDate | day (638) | Date (from calendar.csv), Year, Month, Month_Num |
| StoreProduct *(built in Power Query)* | store x product | Store_ID, Product_ID, Stock_On_Hand, Daily_Profit_90d, Daily_Units_90d |

Relationships (all one-to-many, single direction): DimDate[Date] -> FactSales[Date]; DimStore[Store_ID] -> FactSales, FactInventory; DimProduct[Product_ID] -> FactSales, FactInventory.

## Power Query cleaning steps
1. **Products:** strip `$` and spaces from Product_Cost and Product_Price, change type to Decimal.
2. **Stores:** replace `Cuidad de Mexico` with `Ciudad de Mexico` in Store_City (BR-08).
3. **Calendar:** the file starts with a hidden BOM character, so rename the first column to `Date`; the dates are `M/D/YYYY`, so set the locale to English (United States) when converting the type.
4. **Sales:** set Date to Date, remove no rows (there are no nulls or duplicates).
5. **StoreProduct:** group FactSales rows from 2023-07-03 onward by Store_ID and Product_ID (sum of Units x price minus cost, and sum of Units), divide by 90, then left-merge onto FactInventory.

## Reference measures (DAX)
```dax
Revenue      = SUMX ( FactSales, FactSales[Units] * RELATED ( DimProduct[Unit_Price] ) )
Cost         = SUMX ( FactSales, FactSales[Units] * RELATED ( DimProduct[Unit_Cost] ) )
Profit       = [Revenue] - [Cost]
Margin %     = DIVIDE ( [Profit], [Revenue] )
Units        = SUM ( FactSales[Units] )

Revenue SPLY = CALCULATE ( [Revenue], SAMEPERIODLASTYEAR ( DimDate[Date] ) )
Profit SPLY  = CALCULATE ( [Profit],  SAMEPERIODLASTYEAR ( DimDate[Date] ) )
Revenue LFL % = DIVIDE ( [Revenue] - [Revenue SPLY], [Revenue SPLY] )
Profit LFL %  = DIVIDE ( [Profit]  - [Profit SPLY],  [Profit SPLY] )

Stores in slice   = DISTINCTCOUNT ( FactSales[Store_ID] )
Profit per store  = DIVIDE ( [Profit], [Stores in slice] )

Stock value      = SUMX ( FactInventory, FactInventory[Stock_On_Hand] * RELATED ( DimProduct[Unit_Cost] ) )
Stockout pairs   = COUNTROWS ( FILTER ( FactInventory, FactInventory[Stock_On_Hand] = 0 ) )
Stockout rate %  = DIVIDE ( [Stockout pairs], COUNTROWS ( FactInventory ) )
Profit at risk 30d = SUMX ( FILTER ( StoreProduct, StoreProduct[Stock_On_Hand] = 0 ), StoreProduct[Daily_Profit_90d] * 30 )
Slow stock capital = SUMX ( FILTER ( StoreProduct, StoreProduct[Daily_Units_90d] > 0
                        && DIVIDE ( StoreProduct[Stock_On_Hand], StoreProduct[Daily_Units_90d] ) > 180 ),
                        StoreProduct[Stock_On_Hand] * RELATED ( DimProduct[Unit_Cost] ) )
```
**Margin bridge:** the contribution of a product is `(revenue share now - revenue share before) x (product margin - blended margin before)`. Build it as a small calculated table over the two like-for-like periods, or reuse the values in `../data/summary/margin_bridge_jan_sep.csv`, and check that the contributions add up to the total margin change.

## Pages
| # | Page title (the question it answers) | Visuals | Notes |
|---|---|---|---|
| 1 | Is growth healthy? | Tiles: Revenue, Profit, Margin %, LFL revenue %, LFL profit %; monthly revenue columns; monthly margin line (separate chart) | Show margin change in pp |
| 2 | What moved the margin? | Margin bridge (diverging bars, orange = drag, blue = lift); category revenue share vs profit share; product table (profit, margin, share) | Emphasise Colorbuds and Magic Sand |
| 3 | Which stores and locations earn the most? | Profit per store by location type; top and bottom 5 stores; map optional | Show store count next to each bar |
| 4 | Where are we out of stock? | Tiles: stock value, stockout rate, profit at risk; table of out-of-stock products by profit at risk; slow-stock count | Label the estimate; page ignores date filter |
| 5 | How is everything defined? | KPI dictionary table; data-quality notes | Link from every page |

**Global filters (one row, top):** date range, category, location type, city, store.
**Colours:** blue `#1f6fd0` for the main series, orange `#d1571a` for the comparison or drag, grey for context. This pair passed a colour-blind and contrast check.
**Chart rules:** no dual axes; thin marks; direct labels only on the story (for example Colorbuds and Magic Sand); a table view for every chart.

## Reconciliation table (your measures must return these)
| Check | Expected value |
|---|---|
| Revenue, all data | $14,444,572 |
| Profit, all data | $4,014,029 |
| Margin %, all data | 27.8% |
| Units, all data | 1,090,565 |
| Jan-Sep 2022 revenue / profit | $5,320,116 / $1,572,037 |
| Jan-Sep 2023 revenue / profit | $6,962,074 / $1,824,242 |
| Like-for-like revenue / profit growth | +30.9% / +16.0% |
| Like-for-like margin | 29.5% (2022) to 26.2% (2023) |
| Profit per store: Airport / Downtown / Commercial / Residential | $126,016 / $77,542 / $77,239 / $76,731 |
| Stock value at cost | $300,210 |
| Out-of-stock store x product pairs | 77 of 1,593 (4.8%) |
| Estimated profit at risk, 30 days | $9,685 |
| Slow-stock pairs / capital | 50 / $15,177 |
| Store x product pairs missing from inventory | 157 (41 of them have sales) |

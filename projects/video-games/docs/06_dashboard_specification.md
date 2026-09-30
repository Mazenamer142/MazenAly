# 06 | Power BI dashboard specification

This is an exploration dashboard, not a monitoring one. The user is looking around to make a decision, so the slicers matter more than the KPIs. The DAX is a first draft, not tested in Power BI yet.

## Pages
| Page | Question | Visuals |
|---|---|---|
| 1. Market | How big is each genre? | KPI cards, genre bars, average per game, year slicer |
| 2. Regions | Who buys what, where? | Genre x region heat map, region toggle |
| 3. Hits and quality | How spread out are sales? Do scores matter? | Top-N share, critic score bands, million-seller rate |
| 4. Platforms and publishers | Where should we launch? Who competes? | Platform family bars, console bars, top 10 publishers |
| 5. Data limits | Can I trust this? | Coverage by year, the limits table, definitions |

## Data model
**fact_games** (one row per game on a console) connects to **dim_genre**, **dim_platform** (console and family), **dim_publisher** (with the merge table) and **dim_year**. Region sales are kept as 4 columns and also unpivoted into a small **fact_region** table so one region slicer can drive all charts.

## Draft measures
```
Total sales (M) = SUM ( fact_games[sales] )
Games = COUNTROWS ( fact_games )
Avg per game (M) = DIVIDE ( [Total sales (M)], [Games] )
Million sellers = CALCULATE ( [Games], fact_games[sales] >= 1 )
Region share of genre =
    DIVIDE ( CALCULATE ( SUM ( fact_region[sales] ) ), CALCULATE ( SUM ( fact_region[sales] ), ALL ( dim_genre ) ) )
```

## Design notes
- The year slicer defaults to 1995 to 2018 and shows a warning outside it.
- Every average is shown next to the game count so nobody reads a big number from three games.
- Colour: one blue ramp for heat maps, one accent colour for the selected genre.

## Reconciliation table
| Check | Expected |
|---|---|
| Games with sales | 18,922 |
| Total sales | 6,605.9M |
| Genre share, Sports / Action / Shooter | 18.0% / 17.0% / 15.1% |
| Region totals NA / Europe & Africa / Japan / Other | 3,346M / 1,917M / 688M / 651M |
| Top 100 games' share of sales | 12.0% |
| Top 10 publishers' share (after merge) | 61.7% |

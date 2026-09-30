# 03 | Build guide: coffee shop operations dashboard

About 45 to 60 minutes if you have done Power BI before. Do 01 and 02 first, then apply `theme.json` (**View > Themes > Browse for themes**).

Page size: 16:9 (default). Set **View > Page view > Fit to page**. Use a title text box on every page: 20 pt, bold.

## Page 1: Trading (How are we doing?)
| Visual | Fields | Notes |
|---|---|---|
| Card x4 | `Revenue`, `Revenue per day`, `Units`, `Sale lines` | Top row |
| Clustered column chart | X: `dim_date[month]`, Y: `Revenue per day` | Data labels on. Title: "Revenue per day, by month" |
| Card | `Revenue per day, change vs last month` | Format as percent, conditional colour: green above 0 |
| Slicer (tiles) | `fact_sales[store_location]` | Left side |
| Slicer (dropdown) | `dim_date[month]` | Left side |

## Page 2: The day (When are we busy?)
| Visual | Fields | Notes |
|---|---|---|
| Line chart | X: `dim_hour[label]`, Y: `Revenue per day`, Legend: `fact_sales[store_location]` | Turn off markers. Title: "Revenue by hour of the day" |
| Matrix (heat map) | Rows: `dim_date[weekday]`, Columns: `dim_hour[label]`, Values: `Revenue` | Format > Cell elements > Background colour > fx > Gradient (light blue to dark blue) |
| Clustered bar | Axis: `dim_hour[block]`, Values: `Revenue`, Legend: `store_location` | Or a matrix of `Morning rush share` by store |
| Card x2 | `Morning rush share`, `Evening share (after 5pm)` | |
| Slicer | `fact_sales[store_location]` | Sync with page 1: View > Sync slicers |

## Page 3: The menu (What do they buy?)
| Visual | Fields | Notes |
|---|---|---|
| Bar chart | Axis: `product_category`, Values: `Revenue` | Sort descending |
| Bar chart | Axis: `product_type`, Values: `Revenue` | Filter pane: Top N = 8 by `Revenue` |
| Donut or bar | Legend: `size`, Values: `Sale lines` | Visual filter: `size` is not "No size" |
| Table | `product_detail`, `Units`, `Revenue` | Top N = 10 by `Revenue` |
| Cards | `Drinks share`, `Small drinks share` | |

## Page 4: About the data (Can I trust it?)
Text boxes only: the KPI dictionary from `docs/04_kpi_dictionary.md` and the data limits (six months, no costs, no receipt id, 15 products with a second price). Add a link to the raw data on the portfolio.

## Check your numbers (the acceptance test)
Clear all slicers, then check. If one is off, the model is wrong, not the visual.

| Check | Should show |
|---|---|
| Sale lines | 149,116 |
| Units | 214,470 |
| Revenue | $698,812 |
| Revenue per day | $3,861 |
| Revenue per day, January / June | $2,635 / $5,550 |
| Revenue: Astoria / Hell's Kitchen / Lower Manhattan | $232,244 / $236,511 / $230,057 |
| Morning rush share, all stores | 45.8% |
| Morning rush share: Astoria / Hell's Kitchen / Lower Manhattan | 38.5% / 48.2% / 50.7% |
| Evening share: Astoria / Hell's Kitchen / Lower Manhattan | 21.0% / 16.1% / 8.3% |
| Drinks share | 77.1% |
| Small drinks share | 13.3% |

## Publish and embed
1. **Home > Publish** to a workspace. Publishing needs a work or school Microsoft account.
2. In the Power BI service open the report: **File > Embed report > Publish to web (public)**. Your admin can turn this off.
3. Copy the link into `window.PB_EMBEDS.coffee` at the bottom of `index.html`.
4. If publishing is blocked, export each page as a PNG (**File > Export**), and record a 2 minute walkthrough video instead. Put the `.pbix` in the repo.

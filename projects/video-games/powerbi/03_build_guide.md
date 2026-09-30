# 03 | Build guide: video game market explorer

An exploration dashboard, so the slicers matter more than the cards. About 60 to 75 minutes. Do 01 and 02 first, then apply `theme.json` (**View > Themes > Browse for themes**). Put a **Release year** range slicer (`fact_games[release_year]`, between) and a **Genre** list slicer in the left column of every page, and sync them (**View > Sync slicers**). Default the year range to 1995 to 2018.

## Page 1: Market (How big is each genre?)
| Visual | Fields | Notes |
|---|---|---|
| Card x4 | `Total sales (M)`, `Games`, `Avg per game (M)`, `Million seller rate` | |
| Bar chart | Axis: `genre`, Values: `Total sales (M)` | Sort descending, top 10 |
| Bar chart | Axis: `genre`, Values: `Avg per game (M)` | Same order. Add `Games` as a tooltip so nobody reads a big average from 3 games |

## Page 2: Regions (Who buys what, where?)
| Visual | Fields | Notes |
|---|---|---|
| Matrix (heat map) | Rows: `fact_games[genre]`, Columns: `fact_region[region]`, Values: `Genre share of region` | Cell background: gradient light to dark blue. Top 8 genres by `Total sales (M)` |
| Column chart | Axis: `fact_region[region]`, Values: `Region sales (M)` | Region totals |
| Slicer (tiles) | `fact_region[region]` | |

## Page 3: Hits and quality (How spread out are sales? Do scores matter?)
| Visual | Fields | Notes |
|---|---|---|
| Card x2 | `Million sellers`, `Million seller rate` | |
| Column chart | Axis: `score_band` (sorted by `band_order`), Values: `Avg per scored game (M)` | Visual filter: `score_band` is not "No score". Tooltip: `Games with a score` |
| Table | `title`, `console`, `total_sales` | Top N = 10 by `total_sales` |

## Page 4: Platforms and publishers (Where to launch, and who competes?)
| Visual | Fields | Notes |
|---|---|---|
| Bar chart | Axis: `platform_family`, Values: `Total sales (M)` | |
| Bar chart | Axis: `console`, Values: `Total sales (M)` | Top N = 10 |
| Bar chart | Axis: `publisher_clean`, Values: `Total sales (M)` | Top N = 10 |
| Card | `Top 10 publisher share` | |

## Page 5: Data limits (Can I trust it?)
Text boxes: the limits table from `docs/03_data_limits_and_assumptions.md`. If you loaded `fact_all_rows`, add a column chart of the share of rows with a sales number by release year (2012 to 2024): it shows the fall to 3% in 2019. Add a big warning text box: "Sales stop around 2018."

## Check your numbers (the acceptance test)
Year slicer wide open (clear it), no genre selected.

| Check | Should show |
|---|---|
| Games (with sales) | 18,922 |
| Total sales | 6,605.9M |
| Avg per game | 0.35M |
| Million sellers / rate | 1,505 / 8.0% |
| Sports: sales / games / avg per game | 1,187.5M / 2,597 / 0.46M |
| Shooter avg per game | 0.67M |
| Genre share of region: Role-Playing in Japan | 19.0% |
| Genre share of region: Shooter in Japan | 4.9% |
| Region totals: NA / Europe & Africa / Japan / Other | 3,346M / 1,917M / 688M / 651M |
| Critic band over 9: games / average | 194 / 2.48M |
| Electronic Arts sales (after the merge) | 1,157.3M |
| Top 10 publisher share | 61.7% |

Note that Total sales, the genre share of region and the region totals may differ by 1 or 2 in the last digit because of rounding.

## Publish and embed
1. **Home > Publish** (work or school Microsoft account needed).
2. In the service: **File > Embed report > Publish to web (public)**. Your admin can turn this off.
3. Copy the link into `window.PB_EMBEDS.games` at the bottom of `index.html`.
4. If publishing is blocked: export pages as PNG, record a short walkthrough, and put the `.pbix` in the repo.

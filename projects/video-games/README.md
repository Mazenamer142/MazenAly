# Video games: what actually sells

A data analysis and business analysis case study on the public **VGChartz video game sales** file (2024 version): 64,016 rows, of which 18,922 (30%) have a sales number.
There is no client. The publisher and its decision are a scenario, and are labelled that way.

## The question
Which genres and platforms have sold the most, and where? How much does a critic score matter?

## What I found
- **Sports, Action and Shooter are 50% of all copies** (6.6 billion with a sales number). Shooter has the best average per game (0.67M) of the big genres.
- **Hits carry the market.** The median game sold 120,000 copies (the mean is 350,000). The top 100 games are 12% of sales; 45% of games sold under 100,000.
- **Japan buys a different mix.** Role-Playing is 19% of Japan's sales and 5% of North America's. Shooters are under 5% in Japan.
- **Scores help but do not guarantee.** Games over 9 average 2.5M copies, about eight times a game scoring 6 or less. Only 22% of games have a score.
- **Publishers.** The top 10 hold 61.7% of copies once 13 duplicate publisher names are merged.

## Limits
Sales stop around 2018 (3% of 2019 games have sales, none from 2021), so this describes the market up to 2018. 70% of rows have no sales number; I did not fill them in. There is no cost, price or digital data.

## What is in this folder
| Folder | What |
|---|---|
| `sql/` | Five SQL scripts (SQLite): checks and clean tables, coverage, genre and region, hits and critics, platforms and publishers |
| `python/analysis.py` | Repeats the analysis in pandas, runs the SQL, and stops with an error if the two disagree. Writes `data/summary/` |
| `data/summary/` | The small result tables the portfolio charts are drawn from |
| `docs/` | The business analysis package: decision framing, stakeholders, data limits, KPI dictionary, requirements and test cases, Power BI market explorer spec |

## Run it
```
pip install pandas numpy
python python/analysis.py --data "path/to/vgchartz-2024.csv"
```
The raw file is a public download and is not stored in this repo (`data/raw/` is git-ignored).

## Status
The Power BI market explorer is the centrepiece of the business analysis side and is still to be built. When it is published, paste its link into `window.PB_EMBEDS` at the bottom of `index.html`.

AI note: I used AI to help brainstorm and to polish the writing and code in this project.

## The raw data
The raw files are in `assets/data/raw/video-games-data.zip` at the root of this repo, and can be downloaded from the case study page. `python/explore.py` prints the first rows, `info()`, `describe()` and a few pandas checks for every table: `python python/explore.py --data "path/to/unzipped/folder"`.

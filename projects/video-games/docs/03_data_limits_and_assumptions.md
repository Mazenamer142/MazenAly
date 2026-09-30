# 03 | Data limits and assumptions

This is the most important document in the package. If the limits are not written down, the dashboard can mislead people.

## What is missing
| Limit | Size | Effect | How I handled it |
|---|---|---|---|
| Sales blank for most rows | 70% of rows | Any average is for games that have sales, not for every game | All numbers say "games with sales data" |
| Sales stop around 2018 | 3% of 2019 games have sales, 0% from 2021 | No view of recent years, and no view of the current console generation | Charts and findings stop at 2018 |
| Critic score only for some games | 4,126 of 18,922 | Score analysis covers about 1 in 5 games | Said on the page; not used for the whole market |
| Release date missing | 90 sales rows | Left out of the year chart only | Kept in all other totals |
| Title on several consoles | 12,992 titles vs 18,922 rows | One game can count on 3 consoles | Rows are "game on a console"; unique titles are shown too |
| Same company, different names | 13 names merged | Electronic Arts was split from EA Sports | Small merge table (13 names), listed in the SQL |

## What I did not clean
- I did not fill in missing sales. Guessing them would make the numbers look better than the data is.
- Sales of exactly 0.00 (1,352 rows) are kept. They mean under about 5,000 copies, after rounding.

## Business rules
| ID | Rule |
|---|---|
| BR-01 | Only rows with a sales value are in the market totals |
| BR-02 | Region shares are calculated inside each region (a genre's share of Japan's sales, not of world sales) |
| BR-03 | Critic score bands are: 6 or less, 6 to 7, 7 to 8, 8 to 9, over 9 |
| BR-04 | Publisher names are merged with the 13-name table in the SQL |
| BR-05 | Platform families: PlayStation, Xbox, Nintendo, Sega, PC, Other |

## Questions I would ask the data owner
1. Why do sales stop in 2018? Is it a source change, or are newer sales just not tracked yet?
2. Are blank sales unknown, or really zero?
3. Can we get digital sales?

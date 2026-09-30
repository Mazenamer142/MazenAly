# 05 | Requirements and user stories

Priorities use MoSCoW: Must, Should, Could, Won't (for now).

## Business rules
| ID | Rule |
|---|---|
| BR-01 | Revenue = quantity x unit price, using each line's own price |
| BR-02 | Compare months with revenue per day, not monthly totals |
| BR-03 | The "busy hours" of a store are the hours with the highest revenue per day for that store; the first version uses the top 4 |
| BR-04 | Drink size comes from the last word of the product name (Sm, Rg, Lg). Products with no size are shown as "No size" |
| BR-05 | Weekday follows the calendar date; a week starts on Monday in the dashboard |

## Functional requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Show total revenue, revenue per day and units for the selected period and store | Must |
| FR-02 | Show revenue by hour, one line per store | Must |
| FR-03 | Show revenue by weekday and hour as a heat map | Should |
| FR-04 | Show category and product type mix | Must |
| FR-05 | Show size mix for drinks | Should |
| FR-06 | Show monthly revenue per day and month-on-month change | Must |
| FR-07 | Slicers for store, month and category | Must |
| FR-08 | A page that explains every KPI and the data limits | Should |
| FR-09 | Export of the hourly table | Could |
| FR-10 | Profit views | Won't (no cost data) |

## Non-functional
- Opens in under 5 seconds, the data set is about 150k rows.
- Works on a laptop and a tablet.
- Colours must work for colour-blind people; every chart has a table view.

## User stories
| # | As a... | I want... | So that... | Acceptance criteria |
|---|---|---|---|---|
| US-1 | Store manager | to see my store's revenue by hour | I can plan my rota | I pick my store and see its hourly values; they sum to my store's revenue |
| US-2 | Ops manager | to compare the 3 stores on one chart | I can see who is busy when | One line per store, same axis, colours consistent |
| US-3 | Owner | to see how each month compares | I know if growth continues | Monthly revenue per day is shown; Feb is not penalised for being short |
| US-4 | Menu lead | to see the size and category mix | I can decide what to keep | Shares add up to 100% |
| US-5 | Finance | the totals to match the till report | I trust the dashboard | The reconciliation table below matches to the dollar |

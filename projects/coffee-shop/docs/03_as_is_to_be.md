# 03 | Current state and future state (AS-IS / TO-BE)

> **Scenario.** The current process is assumed for the scenario. The numbers are from the real data.

## AS-IS: how scheduling works today (assumed)
1. The store manager writes next week's rota by feel, from last week's rota.
2. Opening hours are set once and rarely changed.
3. The owner looks at a total sales number at the end of the month.
4. Menu changes are decided by what the baristas think sells.

**Pain points**
- No view of demand by hour, so the same rota is used for a rush hour and a quiet afternoon.
- Total sales hides the fact that the 3 stores run very different days.
- Growth has doubled the daily volume, but the rota did not change with it.

## What the data shows about the day
| Store | First / last sale hour | Share of revenue 7 to 10am | Share after 5pm |
|---|---|---|---|
| Astoria | 7 / 19 | 38.5% | 21.0% |
| Hell's Kitchen | 6 / 20 | 48.2% | 16.1% |
| Lower Manhattan | 6 / 20 | 50.7% | 8.3% |

## TO-BE: how it should work
1. Managers open the dashboard on Monday and check revenue by hour for their own store.
2. They put the most staff on the 3 or 4 busiest hours and fewer in the quiet middle of the day.
3. The ops manager reviews opening hours every month with the evening numbers in front of them (for example, Lower Manhattan makes about 8% of its revenue after 5pm and next to nothing after 7pm).
4. The menu lead checks size and category mix each month before making menu changes.

## Gap to close
| Gap | Fix |
|---|---|
| No hourly view | Peak-hour page in the dashboard |
| No store comparison | Store page with the same hour chart for all 3 |
| No agreed rules for "busy" | Business rule BR-03 (below in the spec) |

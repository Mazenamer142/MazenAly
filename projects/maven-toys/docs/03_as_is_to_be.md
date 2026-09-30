# 03 | AS-IS and TO-BE

> **Case-study scenario.** The AS-IS is *inferred* from what the dataset contains and lacks, not observed at a real company. It is labelled as an assumption on purpose.

## AS-IS (assumed current state)
1. Sales are exported and reported as **revenue and units** by store and product.
2. Profit and margin are calculated separately, on request, in spreadsheets.
3. Stock levels are a **single snapshot**: there is no daily stock history, so past stockouts cannot be measured.
4. Product decisions are made by looking at **revenue rank**, which puts Lego Bricks (largest revenue) first even though its margin is 12.5%.
5. Store comparisons use **total** profit, which favours location types with more stores.

**Pain points**
| # | Pain point | Evidence in the data |
|---|---|---|
| P1 | Revenue rank hides low-margin products | Lego Bricks: largest revenue ($2.39M), only 7.4% of profit |
| P2 | Margin decline is not visible until someone builds it | Margin fell 29.5% to 26.2% while revenue grew 30.9% |
| P3 | Location comparisons are distorted by store count | Downtown is 56% of profit but has 29 of 50 stores |
| P4 | Stockouts are invisible in time | No stock history; 77 of 1,593 store x product pairs are out of stock right now |
| P5 | The same KPI can mean different things | Store city spelled two ways; cost and price stored as text |

## TO-BE (proposed)
1. One **model** with cleaned dimensions and a single fact table; every KPI defined once (see the KPI dictionary).
2. A **dashboard** with profit and margin beside revenue, the margin bridge, profit per store, and an inventory view ranked by money at risk.
3. A **weekly review**: Merchandising reads the bridge, Inventory works the stockout list, Finance confirms the numbers against the reconciliation table.
4. A **data request** to start storing daily stock and price history, so estimates can become measurements.

## Process map (TO-BE)
```
Source files -> Clean + model -> Validate against reconciliation table -> Refresh dashboard
                                                                            |
      Weekly review  <---------------- Alerts / insights <-----------------+
          |
          +-> Merchandising: mix and range decisions
          +-> Inventory:     restock the top stockouts
          +-> Finance:       confirm numbers, sign off definitions
```

## What changes
| Area | AS-IS | TO-BE |
|---|---|---|
| Ranking of products | By revenue | By profit and margin, with revenue shown for context |
| Margin | On request | Always visible, with a bridge that explains the change |
| Store comparison | Total profit | Profit per store, by location type |
| Inventory | Snapshot, no priority | Ranked by estimated profit at risk |
| KPI definitions | Informal | One dictionary, one model |

# 04 | KPI dictionary

One agreed definition per KPI. "Grain" is the level at which it is calculated; a KPI is always re-aggregated from the base columns, never averaged from an average.

| KPI | Definition | Formula | Grain | Source | Good direction |
|---|---|---|---|---|---|
| Revenue | Sales value at retail price | SUM(units x unit_price) | sale line | sales, products | Up |
| Cost of goods | Cost of units sold | SUM(units x unit_cost) | sale line | sales, products | Context |
| Profit | Revenue minus cost of goods | Revenue - Cost | sale line | sales, products | Up |
| Margin % | Share of revenue kept as profit | Profit / Revenue | any slice | derived | Up |
| Units | Items sold | SUM(units) | sale line | sales | Up |
| Like-for-like growth % | Change vs the same months a year earlier | (Current period / Same months last year) - 1 | period | derived | Up |
| Revenue mix % | A product's or category's share of revenue | Slice revenue / Total revenue | product, category | derived | Context |
| Margin contribution (pp) | Effect of a product's mix shift on blended margin | (Share now - Share before) x (Product margin - Blended margin before) | product | derived | Context |
| Profit per store | Profit divided by number of stores in the group | Profit / distinct stores | location type | sales, stores | Up |
| Stockout rate % | Share of store x product pairs with no stock | Pairs with stock_on_hand = 0 / All pairs | snapshot | inventory | Down |
| Estimated profit at risk (30 days) | Profit likely lost while a pair is out of stock | Avg daily profit (last 90 days) x 30, for pairs with stock = 0 | store x product | inventory, sales | Down |
| Days of cover | How long current stock lasts at the recent rate | Stock on hand / Avg daily units (last 90 days) | store x product | inventory, sales | Target range |
| Slow-stock capital | Money tied up in stock with far too much cover | SUM(stock x unit_cost) where days of cover > 180 | store x product | inventory, sales | Down |

## Reading notes
- **Profit and margin are the headline KPIs.** Revenue alone hides the margin change the business problem is about.
- **Estimates are labelled.** "Profit at risk" is an estimate because stock is a single snapshot with no history.

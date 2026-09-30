# 06 | Requirements, user stories and use cases

> **Case-study scenario.** Requirement IDs, priorities (MoSCoW) and acceptance criteria are written for the scenario in `01_business_case_and_scope.md`.

## Functional requirements
| ID | Requirement | Priority |
|---|---|---|
| FR-01 | The overview page shows Revenue, Profit, Margin %, Units and like-for-like growth as headline tiles | Must |
| FR-02 | Revenue and margin trends over time are shown on **separate** charts, never on one dual-axis chart | Must |
| FR-03 | A category and product view shows revenue share beside profit share and margin % | Must |
| FR-04 | A margin bridge shows each product's contribution (in percentage points) to the like-for-like margin change | Must |
| FR-05 | A location view shows profit per store by location type, plus the top and bottom stores | Must |
| FR-06 | An inventory view shows stock value, stockout rate, estimated profit at risk and slow-stock capital | Must |
| FR-07 | Global filters (date range, category, location type, city, store) apply to every page; the inventory page ignores the date filter because stock is a snapshot | Must |
| FR-08 | Users can drill from category to product to store | Should |
| FR-09 | A definitions page shows each KPI's formula and the data-quality notes (for example missing inventory pairs) | Should |
| FR-10 | Users can export the data behind any table | Could |
| FR-11 | Store managers see only their own store (row-level security) | Won't (this phase) |

## Non-functional requirements
| ID | Requirement | Category |
|---|---|---|
| NFR-01 | KPI values match the reconciliation table in `07_dashboard_specification.md` exactly | Accuracy |
| NFR-02 | Interactions (filter, drill) respond within 3 seconds on the full dataset (proposed target) | Performance |
| NFR-03 | Data refresh runs on a schedule agreed with the data owner (proposed: daily) | Availability |
| NFR-04 | Chart colours are colour-blind safe and every chart has a table view or data labels | Accessibility |
| NFR-05 | Each page answers one question and states that question in its title | Usability |
| NFR-06 | Every KPI has one definition, held in the model and shown on the definitions page | Consistency |
| NFR-07 | The report needs no manual steps between a data refresh and the numbers updating | Maintainability |

## User stories and acceptance criteria
**US-01 (Executive sponsor).** As an executive sponsor, I want to see profit and margin next to revenue, so that I can tell whether growth is healthy.
- *Given* the overview page is open, *when* it loads, *then* Revenue, Profit, Margin % and like-for-like growth are shown for the selected period.
- *Given* margin has fallen versus the same months last year, *then* the tile shows the change in percentage points.

**US-02 (Head of Merchandising).** As Head of Merchandising, I want to see which products moved the margin, so that I can decide what to promote or drop.
- *Given* the margin bridge, *when* I select Jan-Sep, *then* each product's contribution in pp is listed, biggest negative first, and the contributions add up to the total margin change.
- *Given* I click a product, *then* the other visuals filter to that product.

**US-03 (Finance manager).** As the finance manager, I want every KPI defined once, so that numbers agree across reports.
- *Given* the definitions page, *then* each KPI shows its formula, grain and source.
- *Given* the reconciliation table, *then* the report's totals match it to the dollar.

**US-04 (Store operations manager).** As a store operations manager, I want profit per store by location type, so that I can compare like with like.
- *Given* the location view, *then* profit per store is shown for Airport, Downtown, Commercial and Residential, with the number of stores in each.
- *Given* I click a location type, *then* the store table filters to that type.

**US-05 (Inventory planner).** As an inventory planner, I want out-of-stock products ranked by money at risk, so that I can restock the ones that matter first.
- *Given* the inventory view, *then* out-of-stock products are ranked by estimated profit at risk per 30 days, with the number of stores affected.
- *Given* I hover the estimate, *then* a tooltip explains how it is calculated.

**US-06 (Inventory planner).** As an inventory planner, I want to see slow stock, so that I do not tie up money in overstock.
- *Given* the inventory view, *then* pairs with more than 180 days of cover are counted and their stock cost is totalled.

**US-07 (BI / data team).** As the BI team, I want a documented model and measure definitions, so that I can maintain the report.
- *Given* the specification, *then* the tables, relationships, cleaning steps and measures are all listed.

## Use cases
**UC-01 Review margin performance** (Actor: executive sponsor)
- *Precondition:* data is loaded.
- *Main flow:* 1. Open overview. 2. Read the headline tiles. 3. Open the margin and mix page. 4. Read the margin bridge. 5. Note the two biggest drags.
- *Alternate flow:* margin is up, so the bridge shows the biggest positive drivers instead.
- *Postcondition:* the sponsor knows which products explain the margin change.

**UC-02 Investigate a product's profit change** (Actor: Head of Merchandising)
- *Main flow:* 1. Select a product from the bridge. 2. See its profit and units by month. 3. See which stores and locations changed most. 4. Check stock status for the product.
- *Alternate flow:* the product is out of stock in many stores, so the cause may be availability, not demand.
- *Postcondition:* a hypothesis is recorded (demand, availability or range change) and is either tested or handed to the right owner.

**UC-03 Find and act on stockouts** (Actor: inventory planner)
- *Main flow:* 1. Open the inventory page. 2. Sort out-of-stock products by profit at risk. 3. Open the store list for the top product. 4. Raise replenishment for those stores.
- *Alternate flow:* a pair is missing from inventory, so it is flagged as a data gap and sent to Operations.
- *Postcondition:* the highest-value stockouts have an owner and an action.

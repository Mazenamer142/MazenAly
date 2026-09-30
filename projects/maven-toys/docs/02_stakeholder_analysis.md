# 02 | Stakeholder analysis

> **Case-study scenario.** These are roles I assumed for the scenario; they are not real people.

## Stakeholders
| Stakeholder (role) | Interest | Influence | What they need from the solution | How to engage |
|---|---|---|---|---|
| Executive sponsor (COO / MD) | Profit growth, not just sales growth | High | One page that says whether growth is healthy, and why | Monthly summary, agree KPI definitions early |
| Head of Merchandising | Product mix, range decisions | High | Which products to push, promote or drop, ranked by profit and margin | Working sessions on the margin bridge |
| Finance manager | Margin accuracy, one version of the truth | High | Profit and margin that reconcile to the ledger | Sign off the KPI dictionary and business rules |
| Regional / store operations manager | Store performance, location strategy | Medium | Profit per store, by location type, top and bottom stores | Review store and location views |
| Inventory / supply planner | Availability and stock cost | Medium | Stockouts, days of cover, slow stock, ranked by money at risk | Co-design the inventory view; validate the estimate method |
| Store managers | Their own store's results | Low | A simple view of their store vs peers | Later phase; read-only access |
| BI / data team | Maintainable model | Medium | Clear model, refresh rules, measure definitions | Hand over the model spec and DAX |

## Influence / interest grid
| | Low interest | High interest |
|---|---|---|
| **High influence** | Finance manager (keep satisfied on definitions) | Executive sponsor, Head of Merchandising (manage closely) |
| **Low influence** | Store managers (keep informed) | Store operations, inventory planner, BI team (involve in design) |

## Key tensions to manage
- Merchandising may want to grow revenue with volume products, while Finance is asking about margin. The dashboard has to show both without picking a side.
- Inventory wants to avoid stockouts, which can conflict with keeping stock cost low.

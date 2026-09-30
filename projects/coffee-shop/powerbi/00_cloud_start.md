# 00 | Start here: building in the Power BI Service (browser)

The web version has no place for the Power Query code in `01_power_query.md`, so the data prep is already done for you in `coffee_shop_model.xlsx` (same folder). It has three Excel tables:

| Table | What | Rows |
|---|---|---|
| `fact_sales` | Every sale line, plus `revenue`, `hour` and `size` | 149,116 |
| `dim_date` | One row per day, Jan to Jun 2023, with `month` and `weekday` labels | 181 |
| `dim_hour` | One row per hour (6 to 20), with a `label` and a time-of-day `block` | 15 |

The labels are written so they sort correctly without "sort by column": `01 Jan`, `1 Mon`, `06:00`, `2) 7 to 10am`.

## Steps
1. Sign in at app.powerbi.com with a work or school account. Open a workspace (**My workspace** is fine to start).
2. **New > Report > Pick a published semantic model** is not what you want. Use **+ New item > Upload a file** (or **Get data > Files > Local file**) and pick `coffee_shop_model.xlsx`. Choose **Import**.
3. Open the new semantic model, **Open data model** (or **Edit data model**) to reach the model view.
4. **Relationships** (drag one column onto the other):
   - `fact_sales[transaction_date]` to `dim_date[date]`, many to one, single direction
   - `fact_sales[hour]` to `dim_hour[hour]`, many to one, single direction
5. **New measure** for each line in `02_measures.dax` (paste one at a time). The names and formulas are the same as in the desktop version.
6. From the semantic model choose **Create a report** and follow `03_build_guide.md`, page by page.

If a step looks different in your version of the service, send me a screenshot or the exact words on the screen.

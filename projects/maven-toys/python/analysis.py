"""
Maven Toys - analysis pipeline
================================
1. Loads and cleans the raw CSVs (public Maven Analytics "Maven Toys" dataset).
2. Computes every metric in pandas.
3. Runs the SQL scripts in ../sql on the same data (SQLite) and ASSERTS the SQL and pandas answers agree.
4. Writes small summary CSVs (../data/summary) and site_data.json (used by the portfolio page).

Usage:
    python analysis.py --data "path/to/Maven Toys Data"

Needs: pandas, numpy (SQLite ships with Python).
"""
import argparse, json, re, sqlite3
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SQL_DIR = HERE.parent / "sql"
OUT_DIR = HERE.parent / "data" / "summary"


def money(s: pd.Series) -> pd.Series:
    """'$9.99 ' -> 9.99  (the source stores cost/price as text with a $ and a trailing space)."""
    return s.astype(str).str.replace(r"[\$,\s]", "", regex=True).astype(float)


def load(data_dir: Path):
    products = pd.read_csv(data_dir / "products.csv")
    stores = pd.read_csv(data_dir / "stores.csv")
    inventory = pd.read_csv(data_dir / "inventory.csv")
    sales = pd.read_csv(data_dir / "sales.csv")
    return products, stores, inventory, sales


def run_sql_file(con, name):
    """Run a .sql file statement by statement; return the result of every SELECT."""
    text = re.sub(r"--[^\n]*", "", (SQL_DIR / name).read_text())   # strip comments (some contain ';')
    results = []
    for body in [s.strip() for s in text.split(";") if s.strip()]:
        cur = con.execute(body)
        if body.upper().startswith(("SELECT", "WITH")):
            cols = [c[0] for c in cur.description]
            results.append(pd.DataFrame(cur.fetchall(), columns=cols))
    return results


def main(data_dir: Path):
    products_raw, stores_raw, inventory_raw, sales_raw = load(data_dir)

    # ------------------------------------------------------------------ pandas: clean + model
    prod = products_raw.rename(columns={"Product_ID": "product_id", "Product_Name": "product_name", "Product_Category": "category"})
    prod["unit_cost"] = money(products_raw.Product_Cost)
    prod["unit_price"] = money(products_raw.Product_Price)
    prod = prod[["product_id", "product_name", "category", "unit_cost", "unit_price"]]
    prod["margin_pct"] = (prod.unit_price - prod.unit_cost) / prod.unit_price * 100

    st = stores_raw.rename(columns={"Store_ID": "store_id", "Store_Name": "store_name", "Store_City": "city", "Store_Location": "location_type", "Store_Open_Date": "open_date"})
    st["city"] = st.city.replace({"Cuidad de Mexico": "Ciudad de Mexico"})

    f = sales_raw.rename(columns={"Sale_ID": "sale_id", "Date": "sale_date", "Store_ID": "store_id", "Product_ID": "product_id", "Units": "units"})
    f = f.merge(prod[["product_id", "product_name", "category", "unit_cost", "unit_price"]], on="product_id")
    f["revenue"] = f.units * f.unit_price
    f["cost"] = f.units * f.unit_cost
    f["profit"] = f.revenue - f.cost
    f["date"] = pd.to_datetime(f.sale_date)
    f["year"] = f.date.dt.year
    f["month_num"] = f.date.dt.month
    f["year_month"] = f.date.dt.strftime("%Y-%m")
    f = f.merge(st[["store_id", "store_name", "city", "location_type"]], on="store_id")

    inv = inventory_raw.rename(columns={"Store_ID": "store_id", "Product_ID": "product_id", "Stock_On_Hand": "stock_on_hand"})

    dq = {
        "sale_lines": int(len(f)),
        "duplicate_sale_id": int(f.sale_id.duplicated().sum()),
        "null_cells_in_sales": int(sales_raw.isna().sum().sum()),
        "orphan_product_id": int((~sales_raw.Product_ID.isin(prod.product_id)).sum()),
        "orphan_store_id": int((~sales_raw.Store_ID.isin(st.store_id)).sum()),
        "inventory_rows": int(len(inv)),
        "inventory_rows_possible": int(len(st) * len(prod)),
    }

    # ------------------------------------------------------------------ pandas: metrics
    tot = f[["revenue", "cost", "profit", "units"]].sum()
    overview = {
        "sale_lines": int(len(f)), "first_day": str(f.date.min().date()), "last_day": str(f.date.max().date()),
        "stores": int(st.store_id.nunique()), "products": int(prod.product_id.nunique()),
        "revenue": round(tot.revenue), "cost": round(tot.cost), "profit": round(tot.profit),
        "units": int(tot.units), "margin_pct": round(tot.profit / tot.revenue * 100, 1),
    }

    monthly = f.groupby("year_month").agg(revenue=("revenue", "sum"), profit=("profit", "sum")).reset_index()
    monthly["margin_pct"] = (monthly.profit / monthly.revenue * 100).round(1)

    lfl = f[f.month_num <= 9].groupby("year").agg(revenue=("revenue", "sum"), profit=("profit", "sum"), units=("units", "sum"))
    lfl["margin_pct"] = (lfl.profit / lfl.revenue * 100).round(1)
    growth = {
        "revenue_growth_pct": round((lfl.revenue[2023] / lfl.revenue[2022] - 1) * 100, 1),
        "profit_growth_pct": round((lfl.profit[2023] / lfl.profit[2022] - 1) * 100, 1),
        "margin_2022": float(lfl.margin_pct[2022]), "margin_2023": float(lfl.margin_pct[2023]),
        "revenue_2022": round(lfl.revenue[2022]), "revenue_2023": round(lfl.revenue[2023]),
        "profit_2022": round(lfl.profit[2022]), "profit_2023": round(lfl.profit[2023]),
    }

    cat = f.groupby("category").agg(revenue=("revenue", "sum"), profit=("profit", "sum")).reset_index()
    cat["margin_pct"] = (cat.profit / cat.revenue * 100).round(1)
    cat["revenue_share_pct"] = (cat.revenue / cat.revenue.sum() * 100).round(1)
    cat["profit_share_pct"] = (cat.profit / cat.profit.sum() * 100).round(1)
    catlfl = f[f.month_num <= 9].pivot_table(index="category", columns="year", values="profit", aggfunc="sum")
    cat = cat.merge(((catlfl[2023] / catlfl[2022] - 1) * 100).round(0).rename("profit_change_pct").reset_index(), on="category")
    cat = cat.sort_values("profit", ascending=False)

    pr = f.groupby(["product_id", "product_name", "category"]).agg(revenue=("revenue", "sum"), profit=("profit", "sum")).reset_index()
    pr["margin_pct"] = (pr.profit / pr.revenue * 100).round(1)
    pr["profit_share_pct"] = (pr.profit / pr.profit.sum() * 100).round(1)
    pr = pr.sort_values("profit", ascending=False)
    pr["cumulative_profit_pct"] = (pr.profit.cumsum() / pr.profit.sum() * 100).round(1)

    # product change in profit, Jan-Sep 2022 -> 2023, and the margin bridge (mix effect)
    lf = f[f.month_num <= 9]
    pp = lf.pivot_table(index=["product_name", "category"], columns="year", values=["revenue", "profit", "units"], aggfunc="sum").fillna(0)
    prodchg = pd.DataFrame({
        "profit_2022": pp[("profit", 2022)], "profit_2023": pp[("profit", 2023)],
        "units_2022": pp[("units", 2022)], "units_2023": pp[("units", 2023)],
    })
    prodchg["profit_change"] = prodchg.profit_2023 - prodchg.profit_2022
    prodchg = prodchg.reset_index().sort_values("profit_change")

    rev22, rev23 = pp[("revenue", 2022)], pp[("revenue", 2023)]
    w22, w23 = rev22 / rev22.sum(), rev23 / rev23.sum()
    pm = prod.set_index("product_name").margin_pct / 100
    blended22 = pp[("profit", 2022)].sum() / rev22.sum()
    bridge = pd.DataFrame({
        "rev_share_2022_pct": w22 * 100, "rev_share_2023_pct": w23 * 100,
        "product_margin_pct": pm.reindex(w22.index.get_level_values(0)).values * 100,
        "contribution_pp": ((w23 - w22).values * (pm.reindex(w22.index.get_level_values(0)).values - blended22)) * 100,
    }, index=w22.index).reset_index().sort_values("contribution_pp")
    assert abs(bridge.contribution_pp.sum() - (growth["margin_2023"] - growth["margin_2022"])) < 0.15, "margin bridge must sum to the margin change"

    loc = f.groupby("location_type").agg(revenue=("revenue", "sum"), profit=("profit", "sum")).reset_index()
    loc["stores"] = loc.location_type.map(st.location_type.value_counts())
    loc["profit_per_store"] = (loc.profit / loc.stores).round(0)
    loc["revenue_per_store"] = (loc.revenue / loc.stores).round(0)
    loc["profit_share_pct"] = (loc.profit / loc.profit.sum() * 100).round(1)
    loc = loc.sort_values("profit_per_store", ascending=False)

    sp = f.groupby(["store_name", "city", "location_type"]).agg(revenue=("revenue", "sum"), profit=("profit", "sum")).reset_index().sort_values("profit", ascending=False)

    dow = f.groupby(f.date.dt.dayofweek).revenue.sum()
    fri_sun_share = round(dow.loc[[4, 5, 6]].sum() / dow.sum() * 100, 1)
    weekday = pd.DataFrame({"weekday": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "revenue": dow.reindex(range(7)).values.round(0)})

    # inventory
    iv = inv.merge(prod, on="product_id")
    iv["value"] = iv.stock_on_hand * iv.unit_cost
    recent = f[f.date >= f.date.max() - pd.Timedelta(days=89)]
    rate = recent.groupby(["store_id", "product_id"]).agg(daily_profit=("profit", "sum"), daily_units=("units", "sum")).reset_index()
    rate[["daily_profit", "daily_units"]] /= 90
    iv = iv.merge(rate, on=["store_id", "product_id"], how="left").fillna({"daily_profit": 0, "daily_units": 0})
    out = iv[iv.stock_on_hand == 0]
    stockouts = out.groupby(["product_name", "category"]).agg(stores_out_of_stock=("store_id", "count"), est_profit_at_risk_per_30d=("daily_profit", lambda s: s.sum() * 30)).reset_index()
    stockouts["margin_pct"] = stockouts.product_name.map(prod.set_index("product_name").margin_pct).round(0)
    stockouts["est_profit_at_risk_per_30d"] = stockouts.est_profit_at_risk_per_30d.round(0)
    stockouts = stockouts.sort_values("est_profit_at_risk_per_30d", ascending=False)
    slow = iv[(iv.daily_units > 0) & (iv.stock_on_hand / iv.daily_units.where(iv.daily_units > 0) > 180)]
    have = set(zip(inv.store_id, inv.product_id)); sold = set(zip(f.store_id, f.product_id))
    allp = {(a, b) for a in st.store_id for b in prod.product_id}
    inventory_kpis = {
        "stock_value_at_cost": round(iv.value.sum()), "stockout_pairs": int(len(out)), "store_product_pairs": int(len(iv)),
        "stockout_rate_pct": round(len(out) / len(iv) * 100, 1), "est_profit_at_risk_per_30d": round(out.daily_profit.sum() * 30),
        "slow_pairs": int(len(slow)), "capital_tied_up": round(slow.value.sum()),
        "pairs_missing_from_inventory": len(allp - have), "missing_pairs_with_sales": len((allp - have) & sold),
    }

    # ------------------------------------------------------------------ SQL: run the scripts, assert they agree with pandas
    con = sqlite3.connect(":memory:")
    products_raw.to_sql("products", con, index=False)
    stores_raw.to_sql("stores", con, index=False)
    inventory_raw.to_sql("inventory", con, index=False)
    sales_raw.to_sql("sales", con, index=False)
    checks = run_sql_file(con, "00_clean_and_model.sql")
    dq_sql = dict(zip(checks[0].check_name, checks[0].result))
    assert dq_sql["sales rows"] == dq["sale_lines"] and dq_sql["duplicate sale_id"] == 0 and dq_sql["orphan store_id"] == 0

    s01 = run_sql_file(con, "01_kpi_overview.sql")
    assert int(s01[0].revenue[0]) == overview["revenue"] and int(s01[0].profit[0]) == overview["profit"], "SQL vs pandas: headline totals"
    assert float(s01[0].margin_pct[0]) == overview["margin_pct"]
    assert len(s01[1]) == len(monthly) and abs(s01[1].revenue.sum() - monthly.revenue.sum()) < 25  # SQL rounds each month to whole dollars

    s02 = run_sql_file(con, "02_category_and_product_mix.sql")
    assert list(s02[0].category) == list(cat.category) and abs(s02[0].profit.sum() - cat.profit.sum()) < 5, "SQL vs pandas: category"
    assert list(s02[1].product_name[:5]) == list(pr.product_name[:5]), "SQL vs pandas: product ranking"

    s03 = run_sql_file(con, "03_growth_and_margin_bridge.sql")
    l = s03[0].set_index("year")
    assert int(l.revenue[2023]) == growth["revenue_2023"] and int(l.profit[2022]) == growth["profit_2022"], "SQL vs pandas: like-for-like"
    assert s03[1].sort_values("profit_change").product_name.iloc[0] == prodchg.product_name.iloc[0], "SQL vs pandas: biggest profit decline"
    assert abs(s03[2].contribution_pp.sum() - bridge.contribution_pp.sum()) < 0.05, "SQL vs pandas: margin bridge"

    s04 = run_sql_file(con, "04_store_and_location.sql")
    assert dict(zip(s04[0].location_type, s04[0].stores)) == loc.set_index("location_type").stores.to_dict()
    assert abs(float(s04[0].profit_per_store[0]) - float(loc.profit_per_store.iloc[0])) < 1, "SQL vs pandas: profit per store"

    s05 = run_sql_file(con, "05_inventory_and_stockouts.sql")
    k = s05[0].iloc[0]
    assert int(k.stockout_pairs) == inventory_kpis["stockout_pairs"] and int(k.stock_value_at_cost) == inventory_kpis["stock_value_at_cost"], "SQL vs pandas: inventory"
    assert int(s05[1].stores_out_of_stock.sum()) == inventory_kpis["stockout_pairs"]
    assert int(s05[3].pairs_missing_from_inventory[0]) == inventory_kpis["pairs_missing_from_inventory"]
    assert int(s05[2].slow_pairs[0]) == inventory_kpis["slow_pairs"] and abs(float(s05[2].capital_tied_up[0]) - inventory_kpis["capital_tied_up"]) < 5, "SQL vs pandas: slow stock"
    print("OK: SQL results match pandas on totals, mix, growth, bridge, locations and inventory.")

    # ------------------------------------------------------------------ write outputs
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    r0 = lambda d, cols: d.assign(**{c: d[c].round(0) for c in cols})
    r0(monthly, ["revenue", "profit"]).to_csv(OUT_DIR / "monthly.csv", index=False)
    r0(cat, ["revenue", "profit"]).to_csv(OUT_DIR / "category.csv", index=False)
    r0(pr, ["revenue", "profit"]).to_csv(OUT_DIR / "product.csv", index=False)
    r0(prodchg, ["profit_2022", "profit_2023", "profit_change"]).to_csv(OUT_DIR / "product_profit_change_jan_sep.csv", index=False)
    bridge.round(2).to_csv(OUT_DIR / "margin_bridge_jan_sep.csv", index=False)
    r0(loc, ["revenue", "profit"]).to_csv(OUT_DIR / "location_type.csv", index=False)
    r0(sp, ["revenue", "profit"]).to_csv(OUT_DIR / "store_profit.csv", index=False)
    stockouts.to_csv(OUT_DIR / "stockouts.csv", index=False)

    tiny = lambda d, cols: d[cols].to_dict("records")
    site = {
        "overview": overview, "growth": growth, "data_quality": dq, "inventory": inventory_kpis, "fri_sun_share_pct": fri_sun_share,
        "monthly": [{"m": r.year_month, "revenue": round(r.revenue), "margin": r.margin_pct} for r in monthly.itertuples()],
        "category": [{"name": r.category, "rev_share": r.revenue_share_pct, "profit_share": r.profit_share_pct, "margin": r.margin_pct, "profit_change_pct": r.profit_change_pct} for r in cat.itertuples()],
        "product_top": [{"name": r.product_name, "profit": round(r.profit), "margin": r.margin_pct, "profit_share": r.profit_share_pct, "revenue": round(r.revenue)} for r in pr.head(8).itertuples()],
        "pareto": {"top5_profit_share_pct": round(pr.head(5).profit.sum() / pr.profit.sum() * 100, 1), "top10_profit_share_pct": round(pr.head(10).profit.sum() / pr.profit.sum() * 100, 1)},
        "profit_change": [{"name": r.product_name, "change": round(r.profit_change)} for r in pd.concat([prodchg.head(4), prodchg.tail(6)]).itertuples()],
        "bridge": [{"name": r.product_name, "pp": round(r.contribution_pp, 2)} for r in pd.concat([bridge.head(4), bridge.tail(4)]).itertuples()],
        "location": [{"type": r.location_type, "stores": int(r.stores), "profit_per_store": int(r.profit_per_store), "profit_share": r.profit_share_pct} for r in loc.itertuples()],
        "top_stores": [{"name": r.store_name, "type": r.location_type, "profit": round(r.profit)} for r in sp.head(5).itertuples()],
        "weekday": [{"d": r.weekday, "revenue": round(r.revenue)} for r in weekday.itertuples()],
        "stockouts": [{"name": r.product_name, "stores": int(r.stores_out_of_stock), "risk30": int(r.est_profit_at_risk_per_30d), "margin": int(r.margin_pct)} for r in stockouts.head(6).itertuples()],
        "lego": {"revenue": round(pr[pr.product_name == "Lego Bricks"].revenue.iloc[0]), "margin": float(pr[pr.product_name == "Lego Bricks"].margin_pct.iloc[0]), "profit_share": float(pr[pr.product_name == "Lego Bricks"].profit_share_pct.iloc[0])},
    }
    (OUT_DIR / "site_data.json").write_text(json.dumps(site, indent=1))
    print("Wrote summary CSVs and site_data.json to", OUT_DIR)
    print(json.dumps({"overview": overview, "growth": growth, "inventory": inventory_kpis, "fri_sun_share_pct": fri_sun_share}, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(HERE.parent / "data" / "raw"), help="folder containing sales.csv, products.csv, stores.csv, inventory.csv")
    main(Path(ap.parse_args().data))

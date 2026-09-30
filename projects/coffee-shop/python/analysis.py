"""
coffee shop analysis
loads the excel file, works out the numbers in pandas, runs the sql scripts
on the same data and checks the answers match.
writes small summary csvs and site_data.json (used by the portfolio page).

run:  python analysis.py --data "path/to/Coffee Shop Sales.xlsx"
needs pandas, numpy and openpyxl
"""
import argparse, json, re, sqlite3
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SQL_DIR = HERE.parent / "sql"
OUT_DIR = HERE.parent / "data" / "summary"
DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def run_sql_file(con, name):
    """run a sql file one statement at a time, return every select result"""
    text = re.sub(r"--[^\n]*", "", (SQL_DIR / name).read_text())   # drop comments first
    results = []
    for body in [s.strip() for s in text.split(";") if s.strip()]:
        cur = con.execute(body)
        if body.lower().startswith(("select", "with")):
            results.append(pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description]))
    return results


def main(path):
    raw = pd.read_excel(path)
    raw["transaction_date"] = raw.transaction_date.dt.strftime("%Y-%m-%d")
    raw["transaction_time"] = raw.transaction_time.astype(str)

    f = raw.rename(columns={"transaction_id": "sale_id", "transaction_qty": "qty", "product_category": "category", "product_detail": "product"})
    f["revenue"] = f.qty * f.unit_price
    f["date"] = pd.to_datetime(f.transaction_date)
    f["month"] = f.date.dt.strftime("%Y-%m")
    f["hour"] = f.transaction_time.str[:2].astype(int)
    f["weekday_num"] = (f.date.dt.dayofweek + 1) % 7            # 0 = sunday, same as sqlite
    f["size"] = f["product"].str.extract(r" (Sm|Rg|Lg)$")[0].map({"Sm": "Small", "Rg": "Regular", "Lg": "Large"}).fillna("No size")
    n_days = f.date.nunique()

    dq = {
        "sale_lines": int(len(f)),
        "duplicate_ids": int(f.sale_id.duplicated().sum()),
        "null_cells": int(raw.isna().sum().sum()),
        "products": int(f.product_id.nunique()),
        "products_with_2_prices": int((f.groupby("product_id").unit_price.nunique() > 1).sum()),
        "lines_with_odd_price": int((f.unit_price != f.product_id.map(f.groupby("product_id").unit_price.agg(lambda x: x.mode()[0]))).sum()),
        "days": int(n_days),
    }

    overview = {
        "sale_lines": int(len(f)), "units": int(f.qty.sum()), "revenue": round(f.revenue.sum()),
        "first_day": f.transaction_date.min(), "last_day": f.transaction_date.max(), "stores": int(f.store_id.nunique()),
        "revenue_per_day": round(f.revenue.sum() / n_days), "revenue_per_line": round(f.revenue.sum() / len(f), 2),
        "lines_one_unit_pct": round((f.qty == 1).mean() * 100, 1),
    }

    monthly = f.groupby("month").agg(revenue=("revenue", "sum"), days=("date", "nunique")).reset_index()
    monthly["per_day"] = monthly.revenue / monthly.days
    lines_m = f.groupby("month").size().values
    monthly["lines"] = lines_m
    monthly["per_line"] = monthly.revenue / monthly.lines

    hour_store = f.groupby(["store_location", "hour"]).revenue.sum().div(n_days).unstack(0).fillna(0)
    hour_all = f.groupby("hour").revenue.sum()
    rush = f.assign(r=np.where(f.hour.between(7, 10), f.revenue, 0), e=np.where(f.hour >= 17, f.revenue, 0)).groupby("store_location").agg(rev=("revenue", "sum"), r=("r", "sum"), e=("e", "sum"))
    rush["evening_pct"] = rush.e / rush.rev * 100
    rush["morning_rush_pct"] = (rush.r / rush.rev * 100)
    hours_open = f.groupby("store_location").hour.agg(["min", "max"])
    weekday = f.groupby("weekday_num").revenue.sum()
    blocks = {"6am": (6, 6), "7 to 10am": (7, 10), "11am to 1pm": (11, 13), "2 to 4pm": (14, 16), "5 to 6pm": (17, 18), "7 to 8pm": (19, 20)}
    block_share = {st: [round(g[g.hour.between(a, b)].revenue.sum() / g.revenue.sum() * 100, 1) for a, b in blocks.values()] for st, g in f.groupby("store_location")}

    cat = f.groupby("category").revenue.sum().sort_values(ascending=False)
    ptype = f.groupby("product_type").revenue.sum().sort_values(ascending=False)
    top_prod = f.groupby("product").agg(revenue=("revenue", "sum"), units=("qty", "sum")).sort_values("revenue", ascending=False)
    sized = f[f["size"] != "No size"]
    size_share = (sized.groupby("size").size() / len(sized) * 100).sort_values(ascending=False)
    store = f.groupby("store_location").agg(revenue=("revenue", "sum"), lines=("sale_id", "count"))
    store["per_day"] = store.revenue / n_days

    jan, jun = f[f.month == "2023-01"], f[f.month == "2023-06"]
    cg = pd.DataFrame({"jan": jan.groupby("category").revenue.sum() / 31, "jun": jun.groupby("category").revenue.sum() / 30})
    cg["growth_pct"] = (cg.jun / cg.jan - 1) * 100
    cg = cg.sort_values("jun", ascending=False)
    drinks = ["Coffee", "Tea", "Drinking Chocolate"]
    drink_share = round(cat[drinks].sum() / cat.sum() * 100, 1)

    # sql: run the scripts and check they match pandas
    con = sqlite3.connect(":memory:")
    raw.to_sql("sales", con, index=False)
    c0 = run_sql_file(con, "00_clean_and_model.sql")
    assert int(c0[0].iloc[0, 0]) == dq["sale_lines"] and int(c0[1].iloc[0, 0]) == 0 and int(c0[2].iloc[0, 0]) == 0
    assert int(c0[4].iloc[0, 0]) == dq["products_with_2_prices"], "sql vs pandas: products with 2 prices"
    s01 = run_sql_file(con, "01_kpi_overview.sql")
    assert int(s01[0].revenue[0]) == overview["revenue"] and int(s01[0].units[0]) == overview["units"], "sql vs pandas: totals"
    assert int(s01[0].revenue_per_day[0]) == overview["revenue_per_day"]
    assert abs(s01[1].revenue.sum() - monthly.revenue.sum()) < 10 and list(s01[1].days) == list(monthly.days)
    s02 = run_sql_file(con, "02_time_patterns.sql")
    assert abs(s02[0].revenue.sum() - hour_all.sum()) < 20, "sql vs pandas: hours"
    chk = s02[2].set_index("store_location")
    assert (abs(chk.morning_rush_pct - rush.morning_rush_pct.round(1)) < 0.11).all() and (abs(chk.evening_pct - rush.evening_pct.round(1)) < 0.11).all(), "sql vs pandas: rush share"
    assert abs(s02[3].revenue.sum() - weekday.sum()) < 10
    s03 = run_sql_file(con, "03_products_and_categories.sql")
    assert list(s03[0].category) == list(cat.index) and list(s03[1].product_type) == list(ptype.index[:8]), "sql vs pandas: mix"
    assert list(s03[2]["product"][:5]) == list(top_prod.index[:5])
    assert dict(zip(s03[3]["size"], s03[3].lines)) == sized.groupby("size").size().to_dict()
    s04 = run_sql_file(con, "04_stores.sql")
    assert list(s04[0].store_location) == list(store.sort_values("revenue", ascending=False).index)
    assert int(s04[2].set_index("store_location").loc["Lower Manhattan", "first_hour"]) == int(hours_open.loc["Lower Manhattan", "min"])
    s05 = run_sql_file(con, "05_growth.sql")
    g = s05[0].set_index("category")
    assert (abs(g.growth_pct - cg.growth_pct.round(0).reindex(g.index)) <= 1).all(), "sql vs pandas: growth"
    print("OK: sql results match pandas on totals, hours, mix, stores and growth.")

    # outputs
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    monthly.round(2).to_csv(OUT_DIR / "monthly.csv", index=False)
    hour_store.round(1).to_csv(OUT_DIR / "hour_by_store_per_day.csv")
    cat.round(0).to_csv(OUT_DIR / "category.csv")
    ptype.round(0).to_csv(OUT_DIR / "product_type.csv")
    top_prod.head(20).round(0).to_csv(OUT_DIR / "top_products.csv")
    cg.round(1).to_csv(OUT_DIR / "category_growth.csv")
    store.round(0).to_csv(OUT_DIR / "store.csv")

    ML = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    site = {
        "overview": overview, "data_quality": dq,
        "monthly": [{"m": ML[i], "per_day": round(r.per_day), "revenue": round(r.revenue), "per_line": round(r.per_line, 2)} for i, r in enumerate(monthly.itertuples())],
        "hours": [{"h": int(h), "stores": {s: round(float(hour_store.loc[h, s]), 1) if h in hour_store.index else 0 for s in hour_store.columns}} for h in range(6, 21)],
        "rush": [{"store": s, "morning_rush_pct": round(r.morning_rush_pct, 1), "evening_pct": round(r.evening_pct, 1), "first": int(hours_open.loc[s, "min"]), "last": int(hours_open.loc[s, "max"])} for s, r in rush.iterrows()],
        "blocks": {"cols": list(blocks), "stores": block_share},
        "rush_all_pct": round(f[f.hour.between(7, 10)].revenue.sum() / f.revenue.sum() * 100, 1),
        "weekday": [{"d": DAYS[i], "revenue": round(weekday[i])} for i in [1, 2, 3, 4, 5, 6, 0]],
        "category": [{"name": k, "revenue": round(v), "share": round(v / cat.sum() * 100, 1)} for k, v in cat.items()],
        "drink_share_pct": float(drink_share),
        "product_type": [{"name": k, "revenue": round(v)} for k, v in ptype.head(8).items()],
        "top_products": [{"name": k, "revenue": round(r.revenue), "units": int(r.units)} for k, r in top_prod.head(6).iterrows()],
        "size": [{"size": k, "share": round(v, 1)} for k, v in size_share.items()],
        "cat_growth": [{"name": k, "jan": round(r.jan), "jun": round(r.jun), "growth": round(r.growth_pct)} for k, r in cg.iterrows()],
        "stores": [{"name": k, "revenue": round(r.revenue), "per_day": round(r.per_day)} for k, r in store.sort_values("revenue", ascending=False).iterrows()],
    }
    (OUT_DIR / "site_data.json").write_text(json.dumps(site, indent=1))
    print(json.dumps(site, indent=1)[:6000])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(HERE.parent / "data" / "raw" / "Coffee Shop Sales.xlsx"), help="the excel file")
    main(Path(ap.parse_args().data))

"""
video game sales analysis
loads the vgchartz csv, works out the numbers in pandas, runs the sql scripts
on the same data and checks the answers match.
writes small summary csvs and site_data.json (used by the portfolio page).

run:  python analysis.py --data "path/to/vgchartz-2024.csv"
needs pandas and numpy
"""
import argparse, json, re, sqlite3
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SQL_DIR = HERE.parent / "sql"
OUT_DIR = HERE.parent / "data" / "summary"

PUBLISHER_FIX = {
    "EA Sports": "Electronic Arts", "EA Sports BIG": "Electronic Arts",
    "Namco": "Bandai Namco", "Namco Bandai": "Bandai Namco", "Namco Bandai Games": "Bandai Namco", "Bandai": "Bandai Namco",
    "Warner Bros. Interactive": "Warner Bros", "Warner Bros. Interactive Entertainment": "Warner Bros",
    "2K Sports": "2K", "2K Games": "2K",
    "Microsoft Game Studios": "Microsoft", "Microsoft Studios": "Microsoft",
    "Konami Digital Entertainment": "Konami",
}
FAMILY = {}
for fam, cons in {"PlayStation": "PS PS2 PS3 PS4 PSP PSV PSN", "Xbox": "XB X360 XOne XBL",
                  "Nintendo": "NES SNES N64 GC Wii WiiU NS GB GBC GBA DS 3DS VC", "Sega": "GEN SAT DC SCD GG", "PC": "PC OSX"}.items():
    for c in cons.split():
        FAMILY[c] = fam


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
    raw = pd.read_csv(path)
    raw["release_year_all"] = pd.to_datetime(raw.release_date, errors="coerce").dt.year

    s = raw[raw.total_sales.notna()].copy()
    s["publisher"] = s.publisher.replace(PUBLISHER_FIX)
    s["platform_family"] = s.console.map(FAMILY).fillna("Other")
    for c in ["na_sales", "jp_sales", "pal_sales", "other_sales"]:
        s[c] = s[c].fillna(0)
    s["year"] = s.release_date.str[:4].astype("float")           # same as sql: first 4 characters
    s["year"] = s.year.where(s.release_date.notna())

    dq = {
        "rows_in_file": int(len(raw)), "rows_with_sales": int(len(s)), "pct_with_sales": round(len(s) / len(raw) * 100, 1),
        "regions_dont_add_up": int(((s.na_sales + s.jp_sales + s.pal_sales + s.other_sales - s.total_sales).abs() > 0.05).sum()),
        "repeated_title_console": int((s.groupby(["title", "console"]).size() > 1).sum()),
        "sales_rows_without_date": int(s.release_date.isna().sum()),
        "rows_with_score": int(s.critic_score.notna().sum()),
        "publisher_names_merged": len(PUBLISHER_FIX),
    }
    total = s.total_sales.sum()
    overview = {"games": int(len(s)), "unique_titles": int(s.title.nunique()), "total_sales_m": round(total, 1), "median_m": round(s.total_sales.median(), 2)}

    yr = s.dropna(subset=["year"]).groupby("year").total_sales.agg(["count", "sum"])
    cov = raw[raw.release_year_all.between(2012, 2024)].groupby("release_year_all").agg(all_rows=("title", "size"), with_sales=("total_sales", "count"))
    cov["pct"] = cov.with_sales / cov.all_rows * 100

    gen = s.groupby("genre").total_sales.agg(["count", "sum"]).sort_values("sum", ascending=False)
    gen["avg"] = gen["sum"] / gen["count"]
    gen["share"] = gen["sum"] / total * 100
    reg_cols = {"north_america": "na_sales", "europe_africa": "pal_sales", "japan": "jp_sales", "other": "other_sales"}
    regtot = {k: s[c].sum() for k, c in reg_cols.items()}
    gen_reg = pd.DataFrame({k: s.groupby("genre")[c].sum() / regtot[k] * 100 for k, c in reg_cols.items()}).reindex(gen.index)

    ranked = s.total_sales.sort_values(ascending=False).reset_index(drop=True)
    conc = {f"top_{n}_pct": round(ranked.iloc[:n].sum() / total * 100, 1) for n in (10, 100, 1000)}
    hits = {"million_sellers": int((s.total_sales >= 1).sum()), "under_100k": int((s.total_sales < 0.1).sum()), "all_games": int(len(s))}

    sc = s[s.critic_score.notna()].copy()
    sc["band"] = pd.cut(sc.critic_score, [0, 6, 7, 8, 9, 10], labels=["6 or less", "6 to 7", "7 to 8", "8 to 9", "over 9"])
    bands = sc.groupby("band", observed=True).total_sales.agg(["count", "mean"])
    corr = sc[["critic_score", "total_sales"]].corr(method="spearman").iloc[0, 1]

    con_t = s.groupby("console").total_sales.agg(["count", "sum"]).sort_values("sum", ascending=False)
    fam = s.groupby("platform_family").total_sales.sum().sort_values(ascending=False)
    pub = s.groupby("publisher").total_sales.agg(["count", "sum"]).sort_values("sum", ascending=False)
    top10_pub = pub["sum"].head(10).sum() / total * 100

    # sql: run the scripts and check they match pandas
    db = sqlite3.connect(":memory:")
    raw.drop(columns=["release_year_all"]).to_sql("games", db, index=False)
    c0 = run_sql_file(db, "00_clean_and_model.sql")
    assert int(c0[0].iloc[0, 0]) == dq["rows_in_file"] and int(c0[1].rows_with_sales[0]) == dq["rows_with_sales"], "sql vs pandas: row counts"
    assert int(c0[2].iloc[0, 0]) == dq["regions_dont_add_up"] and int(c0[3].iloc[0, 0]) == dq["repeated_title_console"]
    assert int(c0[4].iloc[0, 0]) == dq["sales_rows_without_date"], "sql vs pandas: missing dates"
    s01 = run_sql_file(db, "01_overview_and_coverage.sql")
    assert int(s01[0].titles_on_a_console[0]) == overview["games"] and abs(float(s01[0].total_sales_m[0]) - overview["total_sales_m"]) < 0.11
    assert list(s01[1].release_year) == [int(y) for y in yr.index] and abs(s01[1].sales_m.sum() - yr["sum"].sum()) < 1
    assert list(s01[2].rows_with_sales) == list(cov.with_sales), "sql vs pandas: coverage"
    s02 = run_sql_file(db, "02_genre_and_region.sql")
    assert list(s02[0].genre) == list(gen.index) and abs(s02[0].sales_m.sum() - gen["sum"].sum()) < 1, "sql vs pandas: genres"
    assert abs(s02[1].japan.iloc[0] - gen_reg.japan.iloc[0]) < 0.11 and abs(s02[2].north_america[0] - regtot["north_america"]) < 1
    s03 = run_sql_file(db, "03_hits_and_critics.sql")
    assert abs(float(s03[0].top_100_pct[0]) - conc["top_100_pct"]) < 0.11 and abs(float(s03[0].top_1000_pct[0]) - conc["top_1000_pct"]) < 0.11, "sql vs pandas: concentration"
    assert int(s03[1].million_sellers[0]) == hits["million_sellers"] and int(s03[1].under_100k[0]) == hits["under_100k"]
    assert list(s03[2].games) == list(bands["count"]), "sql vs pandas: critic bands"
    s04 = run_sql_file(db, "04_platforms_and_publishers.sql")
    assert list(s04[0].console) == list(con_t.index[:10]) and list(s04[2].publisher[:5]) == list(pub.index[:5]), "sql vs pandas: platforms and publishers"
    assert abs(float(s04[3].top_10_share_pct[0]) - top10_pub) < 0.11
    print("OK: sql results match pandas on row counts, coverage, genres, hits, critics and publishers.")

    # outputs
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    yr.round(1).to_csv(OUT_DIR / "sales_by_year.csv")
    cov.round(1).to_csv(OUT_DIR / "coverage_by_year.csv")
    gen.round(2).to_csv(OUT_DIR / "genre.csv")
    gen_reg.round(1).to_csv(OUT_DIR / "genre_by_region_pct.csv")
    bands.round(2).to_csv(OUT_DIR / "critic_bands.csv")
    con_t.round(1).to_csv(OUT_DIR / "console.csv")
    pub.head(15).round(1).to_csv(OUT_DIR / "publisher_top15.csv")

    top_g = list(gen.index[:8])
    site = {
        "overview": overview, "data_quality": dq, "concentration": conc, "hits": hits, "critic_corr": round(corr, 2),
        "years": [{"y": int(y), "sales": round(r["sum"], 1), "games": int(r["count"])} for y, r in yr.iterrows() if 1995 <= y <= 2020],
        "coverage": [{"y": int(y), "pct": round(r.pct), "with_sales": int(r.with_sales), "all": int(r.all_rows)} for y, r in cov.iterrows()],
        "genre": [{"name": g, "sales": round(r["sum"], 1), "games": int(r["count"]), "avg": round(r.avg, 2), "share": round(r.share, 1)} for g, r in gen.head(10).iterrows()],
        "genre_region": {"cols": ["North America", "Europe & Africa", "Japan", "Other"], "rows": [{"name": g, "v": [round(gen_reg.loc[g, k], 1) for k in reg_cols]} for g in top_g]},
        "region_total": {k: round(v) for k, v in regtot.items()},
        "critic": [{"band": str(b), "games": int(r["count"]), "avg": round(r["mean"], 2)} for b, r in bands.iterrows()],
        "console": [{"name": c, "sales": round(r["sum"], 1), "games": int(r["count"])} for c, r in con_t.head(10).iterrows()],
        "family": [{"name": k, "sales": round(v, 1), "share": round(v / total * 100, 1)} for k, v in fam.items()],
        "publisher": [{"name": p, "sales": round(r["sum"], 1), "games": int(r["count"])} for p, r in pub.head(10).iterrows()],
        "top10_publisher_pct": round(top10_pub, 1),
    }
    (OUT_DIR / "site_data.json").write_text(json.dumps(site, indent=1))
    for k in ["overview", "data_quality", "concentration", "hits", "critic_corr", "coverage", "genre", "genre_region", "region_total", "critic", "console", "family", "publisher", "top10_publisher_pct"]:
        print(k, json.dumps(site[k]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(HERE.parent / "data" / "raw" / "vgchartz-2024.csv"), help="the csv file")
    main(Path(ap.parse_args().data))

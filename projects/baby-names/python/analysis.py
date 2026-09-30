"""
baby names analysis, 1980 to 2009
loads the csv files, works out every number in pandas, runs the sql scripts on the same data
and checks the answers match. writes small summary csvs, site_data.json (charts on the portfolio page)
and baby-names.json (the name explorer).

run:  python analysis.py --data "path/to/folder with names.csv and regions.csv"
needs pandas and numpy
"""
import argparse, json, re, sqlite3
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SQL_DIR = HERE.parent / "sql"
OUT_DIR = HERE.parent / "data" / "summary"
SITE_ASSETS = HERE.parents[2] / "assets" / "data"
YEARS = list(range(1980, 2010))
DEN = r"(?:aden|ayden|aiden)$"


def run_sql_file(con, name):
    """run a sql file one statement at a time, return every select result"""
    text = re.sub(r"--[^\n]*", "", (SQL_DIR / name).read_text())   # drop comments first
    results = []
    for body in [s.strip() for s in text.split(";") if s.strip()]:
        cur = con.execute(body)
        if body.lower().startswith(("select", "with")):
            results.append(pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description]))
    return results


def eff(births):
    s = births / births.sum()
    return 1 / (s ** 2).sum()


def main(data_dir):
    names_raw = pd.read_csv(data_dir / "names.csv")
    regions_raw = pd.read_csv(data_dir / "regions.csv")

    # ---------------------------------------------------------------- pandas: clean + model
    reg = regions_raw.copy()
    reg["Region"] = reg.Region.replace({"New England": "New_England"})
    reg = pd.concat([reg, pd.DataFrame({"State": ["MI"], "Region": ["Midwest"]})], ignore_index=True)
    f = names_raw.merge(reg, on="State")
    f.columns = [c.lower() for c in f.columns]
    nat = f.groupby(["year", "gender", "name"]).births.sum().reset_index()
    nat["rnk"] = nat.groupby(["year", "gender"]).births.rank(method="min", ascending=False)
    nat["share"] = nat.births / nat.groupby(["year", "gender"]).births.transform("sum")

    dq = {
        "rows_in_file": int(len(names_raw)), "rows_with_nulls": int(names_raw.isna().any(axis=1).sum()),
        "duplicate_rows": int(names_raw.duplicated(["State", "Gender", "Year", "Name"]).sum()),
        "smallest_count": int(names_raw.Births.min()), "states_missing_from_regions": int((~names_raw.State.drop_duplicates().isin(regions_raw.State)).sum()),
        "rows_lost_in_join": int(len(names_raw) - len(f)),
        "pct_rows_under_10": round((f.births < 10).mean() * 100, 1), "pct_births_in_rows_under_10": round(f.births[f.births < 10].sum() / f.births.sum() * 100, 1),
    }
    overview = {
        "rows": int(len(f)), "births": int(f.births.sum()), "unique_names": int(f.name.nunique()), "states": int(f.state.nunique()),
        "girl_names": int(f[f.gender == "F"].name.nunique()), "boy_names": int(f[f.gender == "M"].name.nunique()),
        "girl_births": int(f[f.gender == "F"].births.sum()), "boy_births": int(f[f.gender == "M"].births.sum()),
    }
    by_year = nat.groupby("year").agg(births=("births", "sum"), names=("name", "nunique"))

    # diversity
    div = {}
    for g in "FM":
        d = nat[nat.gender == g].groupby("year").apply(lambda x: pd.Series({
            "unique": len(x), "top10": x.births.nlargest(10).sum() / x.births.sum() * 100, "eff": eff(x.births)}), include_groups=False)
        div[g] = d

    # champions
    top1 = nat[nat.rnk == 1].sort_values(["gender", "year"])
    streaks = {}
    for g in "FM":
        t = top1[top1.gender == g]
        streaks[g] = [{"name": n, "from": int(x.year.min()), "to": int(x.year.max()), "years": int(len(x))} for n, x in t.groupby("name", sort=False)]
        streaks[g].sort(key=lambda s: s["from"])
    first_last = {g: top1[top1.gender == g].iloc[[0, -1]][["year", "name", "share"]].assign(share=lambda d: (d.share * 100).round(2)).to_dict("records") for g in "FM"}

    # churn
    a, b = nat[nat.year == 1980], nat[nat.year == 2009]
    churn = {}
    for g in "FM":
        x, y = a[a.gender == g], b[b.gender == g]
        top100 = len(set(x[x.rnk <= 100].name) & set(y[y.rnk <= 100].name))
        top10 = len(set(x[x.rnk <= 10].name) & set(y[y.rnk <= 10].name))
        t = nat[(nat.gender == g) & (nat.rnk <= 10)]
        seen = set(zip(t.name, t.year))
        new = sum(1 for n, yr in seen if yr > 1980 and (n, yr - 1) not in seen)
        churn[g] = {"top100_kept": top100, "top10_kept": top10, "new_top10_entries": new}
    rise = []
    for g in "FM":
        for r in b[(b.gender == g) & (b.rnk <= 10)].sort_values("rnk").itertuples():
            r80 = a[(a.gender == g) & (a.name == r.name)].rnk
            rise.append({"gender": g, "name": r.name, "rank_2009": int(r.rnk), "rank_1980": int(r80.iloc[0]) if len(r80) else None})

    # rise, fall, spikes
    tot = nat.groupby(["gender", "name"]).births.sum()
    big = tot[tot >= 20000].reset_index()[["gender", "name"]]
    pk = nat.merge(big).sort_values(["births", "year"], ascending=[False, True]).groupby(["gender", "name"]).head(1)
    peak_years = pk.year.value_counts().sort_index()
    prev = nat[["gender", "name", "year", "births"]].copy(); prev["year"] += 1
    j = nat[(nat.year > 1980) & (nat.births >= 1500)].merge(prev.rename(columns={"births": "prev"}), on=["gender", "name", "year"], how="left").fillna({"prev": 0})
    j["jump"] = j.births / (j.prev + 1)
    jumps = j.sort_values("jump", ascending=False).head(8)
    series_names = {"F": ["Jennifer", "Jessica", "Emily", "Emma", "Madison", "Nevaeh"], "M": ["Michael", "Jacob", "Jayden"]}
    series = {}
    for g, ns in series_names.items():
        for n in ns:
            s = nat[(nat.gender == g) & (nat.name == n)].set_index("year").births
            series[n] = [int(s.get(y, 0)) for y in YEARS]

    # gender
    both = nat.groupby("name").gender.nunique()
    pv = nat.pivot_table(index="name", columns="gender", values="births", aggfunc="sum").fillna(0)
    pv["total"] = pv.F + pv.M; pv["girls_pct"] = pv.F / pv.total * 100
    unisex = pv[(pv.total >= 50000) & pv.girls_pct.between(20, 80)].sort_values("total", ascending=False)
    e = nat[nat.year <= 1989].pivot_table(index="name", columns="gender", values="births", aggfunc="sum").fillna(0)
    l = nat[nat.year >= 2000].pivot_table(index="name", columns="gender", values="births", aggfunc="sum").fillna(0)
    e["pct80"] = e.F / (e.F + e.M) * 100; l["pct00"] = l.F / (l.F + l.M) * 100
    flips = pd.concat([e.pct80, l.pct00, pv.total], axis=1).dropna()
    flips = flips[flips.total >= 20000]
    flips["swing"] = flips.pct00 - flips.pct80
    flips = flips.sort_values("swing")

    # sounds
    nat["last"] = nat.name.str[-1].str.lower()
    ends = {g: nat[(nat.gender == g)].assign(n=lambda d: np.where(d["last"] == "n", d.births, 0)).groupby("year").apply(lambda x: x.n.sum() / x.births.sum() * 100, include_groups=False) for g in "FM"}
    lastchg = {}
    for g in "FM":
        x = nat[nat.gender == g].pivot_table(index="last", columns="year", values="births", aggfunc="sum").fillna(0)
        lastchg[g] = ((x[2009] / x[2009].sum() - x[1980] / x[1980].sum()) * 100).sort_values()
    boys = nat[nat.gender == "M"]
    is_den = boys.name.str.contains(DEN, case=False, regex=True)
    den = boys.assign(d=np.where(is_den, boys.births, 0)).groupby("year").apply(lambda x: x.d.sum() / x.births.sum() * 100, include_groups=False)
    den_names = boys[is_den].groupby("name").births.sum().sort_values(ascending=False)
    bn = boys[boys["last"] == "n"].pivot_table(index="name", columns="year", values="births", aggfunc="sum").fillna(0)
    tot_m = boys.groupby("year").births.sum()
    n_chg = ((bn[2009] / tot_m[2009] - bn[1980] / tot_m[1980]) * 100).sort_values(ascending=False)
    avg_len = nat.assign(w=nat.name.str.len() * nat.births).groupby("year").apply(lambda x: x.w.sum() / x.births.sum(), include_groups=False)

    # regions
    rshare = f.groupby("region").agg(states=("state", "nunique"), births=("births", "sum"))
    rshare["share"] = rshare.births / rshare.births.sum() * 100
    rt = f.groupby(["region", "gender", "name"]).births.sum().reset_index()
    a1 = rt.groupby(["gender", "name"]).births.sum().rename("nat_b"); b1 = rt.groupby(["region", "gender"]).births.sum().rename("reg_b"); c1 = rt.groupby("gender").births.sum().rename("all_b")
    x = rt.join(a1, on=["gender", "name"]).join(b1, on=["region", "gender"]).join(c1, on="gender")
    x["lq"] = (x.births / x.reg_b) / (x.nat_b / x.all_b)
    sig = x[x.nat_b >= 30000].sort_values(["region", "lq"], ascending=[True, False]).groupby("region").head(5)
    r09 = f[f.year == 2009].groupby(["region", "gender", "name"]).births.sum().reset_index()
    reg_eff = r09.groupby(["region", "gender"]).births.apply(eff)
    reg_top = r09.sort_values("births", ascending=False).groupby(["region", "gender"]).head(1).set_index(["region", "gender"]).name

    # ---------------------------------------------------------------- SQL: run the scripts, assert they agree with pandas
    con = sqlite3.connect(":memory:")
    names_raw.to_sql("names", con, index=False)
    regions_raw.to_sql("regions", con, index=False)
    c0 = run_sql_file(con, "00_clean_and_model.sql")
    assert int(c0[0].iloc[0, 0]) == dq["rows_in_file"] and int(c0[1].iloc[0, 0]) == 0 and int(c0[2].iloc[0, 0]) == 0, "sql vs pandas: data checks"
    assert int(c0[4].iloc[0, 0]) == dq["states_missing_from_regions"] == 1 and int(c0[-1].iloc[0, 0]) == 0, "sql vs pandas: regions"

    s01 = run_sql_file(con, "01_overview_and_coverage.sql")
    assert int(s01[0].births[0]) == overview["births"] and int(s01[0].unique_names[0]) == overview["unique_names"] and int(s01[0].rows_used[0]) == overview["rows"], "sql vs pandas: totals"
    assert list(s01[1].births) == list(by_year.births) and list(s01[1].unique_names) == list(by_year.names)
    assert dict(zip(s01[2].gender, s01[2].unique_names)) == {"F": overview["girl_names"], "M": overview["boy_names"]}
    assert abs(float(s01[3].pct_rows_under_10[0]) - dq["pct_rows_under_10"]) < .11

    s02 = run_sql_file(con, "02_diversity.sql")[0]
    for g in "FM":
        q = s02[s02.gender == g].sort_values("year")
        assert list(q.unique_names) == list(div[g].unique.astype(int)), "sql vs pandas: unique names"
        assert (abs(q.top10_pct.values - div[g].top10.values) < .06).all() and (abs(q.effective_names.values - div[g].eff.values) <= 1).all(), "sql vs pandas: diversity"

    s03 = run_sql_file(con, "03_rank_and_churn.sql")
    t = s03[0]
    for g in "FM":
        assert list(t[t.gender == g].name) == list(top1[top1.gender == g].name), "sql vs pandas: number one names"
    k = s03[1].set_index("gender")
    assert all(int(k.loc[g, "top100_kept"]) == churn[g]["top100_kept"] and int(k.loc[g, "top10_kept"]) == churn[g]["top10_kept"] for g in "FM"), "sql vs pandas: churn"
    ne = s03[2].set_index("gender").new_top10_entries
    assert all(int(ne[g]) == churn[g]["new_top10_entries"] for g in "FM"), "sql vs pandas: top 10 entries"
    r_sql = s03[3]
    assert [(r.gender, r.name, r.rank_2009) for r in r_sql.itertuples()] == [(r["gender"], r["name"], r["rank_2009"]) for r in rise]
    assert [None if pd.isna(v) else int(v) for v in r_sql.rank_1980] == [r["rank_1980"] for r in rise], "sql vs pandas: 1980 ranks"

    s04 = run_sql_file(con, "04_rise_and_fall.sql")
    assert dict(zip(s04[0].peak_year, s04[0].names)) == {int(y): int(v) for y, v in peak_years.items()}, "sql vs pandas: peak years"
    assert list(s04[1].name) == list(jumps.name) and list(s04[1].year) == list(jumps.year), "sql vs pandas: biggest jumps"
    ser = s04[2]
    for n, vals in series.items():
        q = ser[ser.name == n].set_index("year").births
        assert [int(q.get(y, 0)) for y in YEARS] == vals, "sql vs pandas: name series " + n

    s05 = run_sql_file(con, "05_gender.sql")
    assert int(s05[0].iloc[0, 0]) == int((both == 2).sum()), "sql vs pandas: names used for both"
    assert list(s05[1].name) == list(unisex.index), "sql vs pandas: unisex names"
    fl = s05[2].set_index("name")
    assert set(fl.index) == set(flips.index) and (abs(fl.girls_pct_80s - flips.pct80.reindex(fl.index)) <= 1).all() and (abs(fl.girls_pct_00s - flips.pct00.reindex(fl.index)) <= 1).all(), "sql vs pandas: flips"

    s06 = run_sql_file(con, "06_sounds_and_endings.sql")
    for g in "FM":
        q = s06[0][s06[0].gender == g].sort_values("year")
        assert (abs(q.pct_ends_in_n.values - ends[g].values) < .06).all(), "sql vs pandas: ends in n"
        c = s06[1][s06[1].gender == g].set_index("last_letter").change_pts
        assert (abs(c - lastchg[g].reindex(c.index) ) < .11).all(), "sql vs pandas: last letters"
    assert (abs(s06[2].pct_den_family.values - den.values) < .006).all() and list(s06[3].name) == list(den_names.index[:8]), "sql vs pandas: -den family"
    assert (abs(s06[4].avg_length.values - avg_len.values) < .006).all()
    assert list(s06[5].name) == list(n_chg.index[:8]) and list(s06[6].name) == list(n_chg.index[::-1][:4]), "sql vs pandas: n-ending movers"

    s07 = run_sql_file(con, "07_regions.sql")
    assert list(s07[0].region) == list(rshare.sort_values("births", ascending=False).index)
    assert [(r.region, r.name) for r in s07[1].itertuples()] == [(r.region, r.name) for r in sig.itertuples()], "sql vs pandas: signature names"
    e7 = s07[2].set_index(["region", "gender"]).effective_names
    assert (abs(e7 - reg_eff.reindex(e7.index)) <= 1).all(), "sql vs pandas: regional diversity"
    assert {(r.region, r.gender): r.name for r in s07[3].itertuples()} == reg_top.to_dict(), "sql vs pandas: top names per region"
    print("OK: SQL results match pandas on totals, diversity, ranks, spikes, gender, sounds and regions.")

    # ---------------------------------------------------------------- outputs
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for g in "FM":
        div[g].round(1).to_csv(OUT_DIR / f"diversity_{g}.csv")
    top1[["year", "gender", "name", "births"]].to_csv(OUT_DIR / "number_one_names.csv", index=False)
    jumps[["gender", "name", "year", "births", "prev", "jump"]].round(1).to_csv(OUT_DIR / "biggest_jumps.csv", index=False)
    flips.round(1).to_csv(OUT_DIR / "gender_flips.csv")
    sig.round(2).to_csv(OUT_DIR / "region_signature_names.csv", index=False)
    pd.DataFrame({"ends_in_n_F": ends["F"], "ends_in_n_M": ends["M"], "den_family_M": den, "avg_len": avg_len}).round(2).to_csv(OUT_DIR / "sounds_by_year.csv")

    def rnd(v, d=1):
        return round(float(v), d)
    flip_rows = pd.concat([flips.head(4), flips.tail(6)])
    site = {
        "overview": overview, "data_quality": dq,
        "births_year": [{"y": int(y), "births": int(r.births), "names": int(r.names)} for y, r in by_year.iterrows()],
        "diversity": {g: {"unique": [int(v) for v in div[g].unique], "top10": [rnd(v) for v in div[g].top10], "eff": [int(round(v)) for v in div[g].eff]} for g in "FM"},
        "top1_share": {g: [rnd(v * 100, 2) for v in top1[top1.gender == g].sort_values("year").share] for g in "FM"},
        "boys_recorded_pct": rnd(overview["boy_births"] / overview["births"] * 100),
        "years": YEARS, "streaks": streaks, "first_last": first_last, "churn": churn, "rise": rise,
        "series": series,
        "jumps": [{"gender": r.gender, "name": r.name, "year": int(r.year), "births": int(r.births), "prev": int(r.prev), "jump": rnd(r.jump)} for r in jumps.itertuples()],
        "peak_first_year": int(peak_years.get(1980, 0)), "peak_names_total": int(peak_years.sum()),
        "names_used_for_both": int((both == 2).sum()),
        "unisex": [{"name": n, "girls_pct": int(round(r.girls_pct)), "total": int(r.total)} for n, r in unisex.head(8).iterrows()],
        "flips": [{"name": n, "pct80": int(round(r.pct80)), "pct00": int(round(r.pct00)), "total": int(r.total)} for n, r in flip_rows.iterrows()],
        "ends_n": {g: [rnd(v) for v in ends[g]] for g in "FM"},
        "last_change": {g: {"down": [[k, rnd(v)] for k, v in lastchg[g].head(3).items()], "up": [[k, rnd(v)] for k, v in lastchg[g].tail(3).items()]} for g in "FM"},
        "den": [rnd(v, 2) for v in den], "den_names": [[n, int(v)] for n, v in den_names.head(8).items()],
        "n_movers": {"up": [[n, rnd(v, 2)] for n, v in n_chg.head(8).items()], "down": [[n, rnd(v, 2)] for n, v in n_chg.tail(4).iloc[::-1].items()]},
        "avg_len": {"1980": rnd(avg_len[1980], 2), "2009": rnd(avg_len[2009], 2)},
        "regions": [{"name": r, "states": int(v.states), "share": rnd(v.share)} for r, v in rshare.sort_values("births", ascending=False).iterrows()],
        "signature": {r: [{"name": x.name, "gender": x.gender, "lq": rnd(x.lq)} for x in g.itertuples()] for r, g in sig.groupby("region")},
        "region_eff": {g: [{"name": r, "eff": int(round(reg_eff[(r, g)]))} for r in sorted({k[0] for k in reg_eff.index}, key=lambda r: -reg_eff[(r, g)])] for g in "FM"},
        "region_top": {f"{r}|{g}": n for (r, g), n in reg_top.items()},
    }
    (OUT_DIR / "site_data.json").write_text(json.dumps(site, indent=1))

    # the name explorer: yearly babies for the 3,000 most used names
    top = tot.groupby(level="name").sum().sort_values(ascending=False).head(3000).index
    ex = {}
    piv = nat[nat.name.isin(top)].pivot_table(index=["name", "gender"], columns="year", values="births", aggfunc="sum").fillna(0).astype(int)
    for (n, g), row in piv.iterrows():
        ex.setdefault(n, {})[g.lower()] = [int(row.get(y, 0)) for y in YEARS]
    SITE_ASSETS.mkdir(parents=True, exist_ok=True)
    (SITE_ASSETS / "baby-names.json").write_text(json.dumps({"years": [YEARS[0], YEARS[-1]], "names": ex}, separators=(",", ":")))
    print("wrote summary files and the explorer file (%d names)" % len(ex))
    for k in ["overview", "data_quality", "streaks", "first_last", "churn", "rise", "jumps", "peak_first_year", "peak_names_total", "names_used_for_both", "unisex", "flips", "last_change", "den_names", "avg_len", "n_movers", "regions", "signature", "region_eff", "region_top"]:
        print(k, json.dumps(site[k]))
    print("div", {g: (site["diversity"][g]["unique"][0], site["diversity"][g]["unique"][-1], site["diversity"][g]["top10"][0], site["diversity"][g]["top10"][-1], site["diversity"][g]["eff"][0], site["diversity"][g]["eff"][-1]) for g in "FM"})
    print("ends", site["ends_n"]["M"][0], site["ends_n"]["M"][-1], site["ends_n"]["F"][0], site["ends_n"]["F"][-1], "den", site["den"][0], site["den"][-1])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(HERE.parent / "data" / "raw"), help="folder with names.csv and regions.csv")
    main(Path(ap.parse_args().data))

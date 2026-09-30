"""
first look at the raw data: shape, first rows, info(), describe(), then a few pandas moves.
run:  python explore.py --data "path/to/folder with vgchartz-2024.csv"
needs pandas
"""
import argparse, io
from pathlib import Path
import pandas as pd

FILES = {"games": "vgchartz-2024.csv"}

# small things i check after the first look. each one is a single pandas expression
STEPS = [
    ('missing values per column, in %', '(games.isna().mean() * 100).round(1)'),
    ('how many rows have a sales number?', 'games["total_sales"].notna().sum()'),
    ('releases per year, last 8 years in the file', 'pd.to_datetime(games["release_date"], errors="coerce").dt.year.value_counts().sort_index().tail(8)'),
    ('most common genres', 'games["genre"].value_counts().head(6)'),
    ('how many different consoles?', 'games["console"].nunique()'),
    ('sales by genre, top 5', 'games.groupby("genre")["total_sales"].agg(["count", "sum", "mean"]).round(2).sort_values("sum", ascending=False).head(5)'),
    ('do the four regions add up to the total? (rows that do not)', '(games[["na_sales", "jp_sales", "pal_sales", "other_sales"]].sum(axis=1, min_count=1) - games["total_sales"]).abs().gt(0.05).sum()'),
    ('critic score vs sales (rank correlation)', 'games[["critic_score", "total_sales"]].corr(method="spearman").round(2)')
]


def load(folder):
    """read every file into a dataframe"""
    folder = Path(folder)
    tables = {}
    for name, file in FILES.items():
        path = folder / file
        if not path.exists():
            raise SystemExit(f"cannot find {path}. unzip the data and pass its folder with --data")
        tables[name] = pd.read_csv(path)
    return tables


def summarise(df):
    """the three things i run first on any new table"""
    buf = io.StringIO()
    df.info(buf=buf)
    numbers = df.describe().to_string()
    text = df.select_dtypes(exclude="number")
    words = text.describe().to_string() if text.shape[1] else "no text columns"
    return {"head": df.head(8), "info": buf.getvalue(), "numbers": numbers, "text": words}


def run_steps(tables):
    """run each step in STEPS with the tables (and pandas) available by name"""
    out = []
    for title, code in STEPS:
        result = eval(code, {"pd": pd, **tables})
        out.append((title, code, result.to_string() if hasattr(result, "to_string") else str(result)))
    return out


def main(folder):
    tables = load(folder)
    print("pandas", pd.__version__)
    for name, df in tables.items():
        s = summarise(df)
        print("\n" + "=" * 70)
        print(f"{name}: {df.shape[0]:,} rows x {df.shape[1]} columns")
        print("=" * 70)
        print("\nfirst rows\n" + s["head"].to_string())
        print("\ninfo\n" + s["info"])
        print("describe (numbers)\n" + s["numbers"])
        print("\ndescribe (text)\n" + s["text"])
    print("\n" + "=" * 70 + "\na few pandas moves\n" + "=" * 70)
    for title, code, result in run_steps(tables):
        print(f"\n# {title}\n>>> {code}\n{result}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=".", help="folder with the data files")
    main(ap.parse_args().data)

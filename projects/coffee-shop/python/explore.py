"""
first look at the raw data: shape, first rows, info(), describe(), then a few pandas moves.
run:  python explore.py --data "path/to/folder with Coffee Shop Sales.xlsx"
needs pandas and openpyxl (pip install pandas openpyxl)
"""
import argparse, io
from pathlib import Path
import pandas as pd

FILES = {"transactions": "Coffee Shop Sales.xlsx"}

# small things i check after the first look. each one is a single pandas expression
STEPS = [
    ('empty cells per column', 'transactions.isna().sum()'),
    ('duplicate transaction ids', 'transactions["transaction_id"].duplicated().sum()'),
    ('which dates are in the data?', 'transactions["transaction_date"].agg(["min", "max"])'),
    ('units per line', 'transactions["transaction_qty"].value_counts().sort_index()'),
    ('total revenue (quantity x unit price)', '(transactions["transaction_qty"] * transactions["unit_price"]).sum().round(2)'),
    ('lines per hour of the day', 'pd.to_datetime(transactions["transaction_time"].astype(str), format="%H:%M:%S").dt.hour.value_counts().sort_index()'),
    ('revenue by category', 'transactions.assign(revenue=transactions["transaction_qty"] * transactions["unit_price"]).groupby("product_category")["revenue"].sum().round(0).sort_values(ascending=False)'),
    ('products that have more than one price', '(transactions.groupby("product_id")["unit_price"].nunique() > 1).sum()')
]


def load(folder):
    """read every file into a dataframe"""
    folder = Path(folder)
    tables = {}
    for name, file in FILES.items():
        path = folder / file
        if not path.exists():
            raise SystemExit(f"cannot find {path}. unzip the data and pass its folder with --data")
        tables[name] = pd.read_excel(path)
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

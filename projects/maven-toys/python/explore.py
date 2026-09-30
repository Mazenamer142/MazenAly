"""
first look at the raw data: shape, first rows, info(), describe(), then a few pandas moves.
run:  python explore.py --data "path/to/Maven Toys Data"
needs pandas
"""
import argparse, io
from pathlib import Path
import pandas as pd

FILES = {"sales": "sales.csv", "products": "products.csv", "stores": "stores.csv", "inventory": "inventory.csv"}

# small things i check after the first look. each one is a single pandas expression
STEPS = [
    ('price and cost are text with a $ sign and a trailing space', 'products[["Product_Name", "Product_Cost", "Product_Price"]].head(3)'),
    ('turn the price into a number', 'products["Product_Price"].str.replace("$", "", regex=False).str.strip().astype(float).describe()'),
    ('which dates are in the sales?', 'pd.to_datetime(sales["Date"]).agg(["min", "max"])'),
    ('units per sale line, first 6 values', 'sales["Units"].value_counts().sort_index().head(6)'),
    ('stores by location type', 'stores["Store_Location"].value_counts()'),
    ('sale lines per product, top 5 (merged with the product names)', 'sales.merge(products, on="Product_ID").groupby("Product_Name").size().sort_values(ascending=False).head(5)'),
    ('does every sale have a matching product and store?', '(sales["Product_ID"].isin(products["Product_ID"]).all(), sales["Store_ID"].isin(stores["Store_ID"]).all())'),
    ('memory used by the big table, in MB', '(sales.memory_usage(deep=True).sum() / 1e6).round(1)')
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

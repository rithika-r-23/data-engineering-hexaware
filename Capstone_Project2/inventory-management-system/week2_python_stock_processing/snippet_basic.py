
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

df = pd.read_csv(ROOT / "data" / "raw" / "stock_movements.csv")
df["quantity"] = df["quantity"].astype(int)

stock_summary = df.groupby(["product_id", "warehouse_id"])["quantity"].sum()
low_stock = stock_summary[stock_summary < 10]

print(f"Total stock (numpy sum): {np.sum(stock_summary.to_numpy()):,} units")
print(low_stock)

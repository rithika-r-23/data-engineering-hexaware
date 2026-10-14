from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = HERE / "output"

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%d-%b-%Y", "%d-%m-%Y"]
TYPE_MAP = {
    "IN": "IN", "INBOUND": "IN", "RECEIPT": "IN", "PURCHASE": "IN",
    "OUT": "OUT", "OUTBOUND": "OUT", "SALE": "OUT", "ISSUE": "OUT",
    "ADJUSTMENT": "ADJUSTMENT", "ADJUST": "ADJUSTMENT", "ADJ": "ADJUSTMENT"
}
REQUIRED = ["movement_id", "product_id", "warehouse_id", "movement_type", "quantity", "movement_date"]


def load_movements(path: Path) -> pd.DataFrame:
    path = Path(path)
    if path.suffix.lower() == ".json":
        df = pd.read_json(path, dtype=False).fillna("").astype(str)
    else:
        df = pd.read_csv(path, dtype=str, keep_default_na=False)

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"Input file is missing required columns: {missing}")
    return df


def parse_dates(series: pd.Series) -> pd.Series:
    s = series.astype(str).str.strip()
    parsed = pd.Series(pd.NaT, index=s.index, dtype="datetime64[ns]")

    for fmt in DATE_FORMATS:
        todo = parsed.isna()
        if not todo.any():
            break
        parsed.loc[todo] = pd.to_datetime(s[todo], format=fmt, errors="coerce")

    return parsed


def clean_movements(raw: pd.DataFrame, valid_products, valid_warehouses):
    report = {"rows_loaded": int(len(raw))}
    df = raw.copy()

    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()

    df = df.replace({"": np.nan, "nan": np.nan, "NaN": np.nan, "None": np.nan, "NULL": np.nan})

    for col in ["movement_id", "product_id", "warehouse_id"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    before = len(df)
    df = df.dropna(subset=["movement_id", "product_id", "warehouse_id"])
    report["removed_invalid_ids"] = before - len(df)
    df[["movement_id", "product_id", "warehouse_id"]] = df[
        ["movement_id", "product_id", "warehouse_id"]
    ].astype(int)

    before = len(df)
    df = df.drop_duplicates(subset="movement_id", keep="first")
    report["removed_duplicates"] = before - len(df)

    df["movement_date"] = parse_dates(df["movement_date"])
    before = len(df)
    df = df.dropna(subset=["movement_date"])
    report["removed_bad_dates"] = before - len(df)

    q = df["quantity"].astype(str).str.replace(",", "", regex=False)
    df["quantity"] = pd.to_numeric(q, errors="coerce")
    before = len(df)
    df = df.dropna(subset=["quantity"])
    report["removed_invalid_quantity"] = before - len(df)
    df["quantity"] = df["quantity"].round().astype(int)

    before = len(df)
    df = df[df["quantity"] != 0]
    report["removed_zero_quantity"] = before - len(df)

    df["movement_type"] = df["movement_type"].astype(str).str.upper().map(TYPE_MAP)
    before = len(df)
    df = df.dropna(subset=["movement_type"])
    report["removed_unknown_type"] = before - len(df)

    qty = df["quantity"].to_numpy()
    mtype = df["movement_type"].to_numpy()
    fixed = np.where(mtype == "IN", np.abs(qty), np.where(mtype == "OUT", -np.abs(qty), qty))
    report["sign_corrections"] = int((fixed != qty).sum())
    df["quantity"] = fixed

    before = len(df)
    df = df[
        df["product_id"].isin(valid_products)
        & df["warehouse_id"].isin(valid_warehouses)
    ]
    report["removed_orphans"] = before - len(df)

    for col in ["reference_no", "reason"]:
        if col not in df.columns:
            df[col] = ""
        df[col] = df[col].fillna("")

    df = df.sort_values(["movement_date", "movement_id"]).reset_index(drop=True)
    running = df.groupby(["product_id", "warehouse_id"])["quantity"].cumsum()
    report["rows_negative_running_stock"] = int((running < 0).sum())
    report["rows_after_cleaning"] = int(len(df))

    return df, report


def calculate_stock(clean, products, warehouses, suppliers) -> pd.DataFrame:
    grid = products[["product_id"]].merge(
        warehouses[["warehouse_id"]], how="cross"
    )

    totals = clean.groupby(["product_id", "warehouse_id"], as_index=False).agg(
        quantity_on_hand=("quantity", "sum"),
        last_movement_date=("movement_date", "max")
    )

    stock = grid.merge(totals, on=["product_id", "warehouse_id"], how="left")
    stock["quantity_on_hand"] = stock["quantity_on_hand"].fillna(0).astype(int)

    stock = (
        stock.merge(products, on="product_id")
        .merge(warehouses[["warehouse_id", "warehouse_name"]], on="warehouse_id")
        .merge(suppliers[["supplier_id", "supplier_name"]], on="supplier_id", how="left")
    )

    qoh = stock["quantity_on_hand"].to_numpy()
    low = qoh < stock["reorder_level"].to_numpy()
    over = qoh > stock["max_stock_level"].to_numpy()

    stock["stock_status"] = np.select(
        [low, over], ["LOW_STOCK", "OVERSTOCK"], default="OK"
    )
    stock["shortage_qty"] = np.where(low, stock["reorder_level"] - qoh, 0)
    stock["excess_qty"] = np.where(over, qoh - stock["max_stock_level"], 0)
    stock["suggested_order_qty"] = np.where(low, stock["reorder_quantity"], 0)
    stock["stock_value"] = np.round(qoh * stock["unit_price"].to_numpy(), 2)

    return stock


def build_summary(report, stock) -> str:
    low = stock[stock["stock_status"] == "LOW_STOCK"].sort_values(
        "shortage_qty", ascending=False
    )

    by_wh = (
        stock.groupby(["warehouse_name", "stock_status"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=["LOW_STOCK", "OK", "OVERSTOCK"], fill_value=0)
    )

    cols = [
        "sku", "product_name", "warehouse_name", "quantity_on_hand",
        "reorder_level", "shortage_qty", "suggested_order_qty", "supplier_name"
    ]

    lines = [
        "=" * 78,
        "INVENTORY SUMMARY REPORT (Week 2)",
        "=" * 78,
        "",
        "DATA CLEANING",
        "-" * 78,
        *[f"  {k.replace('_', ' '):<32}{v:>8,}" for k, v in report.items()],
        "",
        "STOCK OVERVIEW",
        "-" * 78,
        f"  product-warehouse combinations : {len(stock):,}",
        f"  total units on hand            : {int(stock['quantity_on_hand'].sum()):,}",
        f"  total stock value (INR)        : {stock['stock_value'].sum():,.2f}",
        f"  LOW_STOCK items                : {(stock['stock_status'] == 'LOW_STOCK').sum():,}",
        f"  OVERSTOCK items                : {(stock['stock_status'] == 'OVERSTOCK').sum():,}",
        "",
        "STATUS BY WAREHOUSE",
        "-" * 78,
        by_wh.to_string(),
        "",
        "TOP 15 LOW-STOCK ITEMS (largest shortage first)",
        "-" * 78,
        low[cols].head(15).to_string(index=False) if len(low) else "  none",
        ""
    ]

    return "\n".join(lines)


def main():
    products = pd.read_csv(RAW_DIR / "products.csv")
    warehouses = pd.read_csv(RAW_DIR / "warehouses.csv")
    suppliers = pd.read_csv(RAW_DIR / "suppliers.csv")

    raw = load_movements(RAW_DIR / "stock_movements_dirty.csv")
    clean, report = clean_movements(
        raw, set(products["product_id"]), set(warehouses["warehouse_id"])
    )
    stock = calculate_stock(clean, products, warehouses, suppliers)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    out = clean.copy()
    out["movement_date"] = out["movement_date"].dt.strftime("%Y-%m-%d")
    out.to_csv(PROCESSED_DIR / "stock_movements_clean.csv", index=False)

    stock_out = stock.copy()
    stock_out["last_movement_date"] = stock_out["last_movement_date"].dt.strftime("%Y-%m-%d")
    stock_out.to_csv(PROCESSED_DIR / "current_stock.csv", index=False)

    report_cols = [
        "product_id", "sku", "product_name", "category", "warehouse_id",
        "warehouse_name", "quantity_on_hand", "reorder_level",
        "shortage_qty", "suggested_order_qty", "supplier_name"
    ]

    stock_out[stock_out["stock_status"] == "LOW_STOCK"].sort_values(
        "shortage_qty", ascending=False
    )[report_cols].to_csv(OUTPUT_DIR / "low_stock_report.csv", index=False)

    stock_out[stock_out["stock_status"] == "OVERSTOCK"].sort_values(
        "excess_qty", ascending=False
    )[
        ["product_id", "sku", "product_name", "warehouse_name",
         "quantity_on_hand", "max_stock_level", "excess_qty"]
    ].to_csv(OUTPUT_DIR / "overstock_report.csv", index=False)

    (OUTPUT_DIR / "cleaning_report.json").write_text(
        json.dumps(report, indent=2)
    )

    summary = build_summary(report, stock)
    (OUTPUT_DIR / "summary_report.txt").write_text(summary, encoding="utf-8")
    print(summary)
    print(f"\nOutputs written to:\n  {OUTPUT_DIR}\n  {PROCESSED_DIR}")


if __name__ == "__main__":
    main()
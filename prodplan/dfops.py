import pandas as pd
from pathlib import Path


def read_to_dataframe(
    path: Path,
    required_column: list,
    column_schema: dict,
    sheet_name: str
) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=sheet_name)
    df = df[required_column]
    df = df.rename(columns=column_schema)
    df = df[(~df["sto_no"].isnull()) & (~df.item_description.isnull()) & (~df.receiving_plant.isnull())]
    return df


def read_weekly_prod(
    path: Path,
    required_column: list,
    column_schema: dict,
    sheet_name: str,
    skip_row=2
) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name=sheet_name, skiprows=skip_row)
    df = df[required_column]
    df = df.rename(columns=column_schema)
    df = df[~df["sto_no"].isnull()]
    df = df[df["sto_no"] != "Total"]
    df["sto_no"] = df["sto_no"].astype(str)
    return df


def create_temp_sto_no(df: pd.DataFrame) -> pd.DataFrame:
    df["temp"] = df["sto_no"].astype('int64').astype('str')
    return df


def make_pgi_qty_df(df: pd.DataFrame) -> pd.DataFrame:
    selected_columns = [
        'sto_no', 'item_description', 'receiving_plant',
        'delivery_no', 'pgi_date', 'pgi_quantity', 'pgi_uom'
    ]
    _df = df[selected_columns].copy()
    _df = create_temp_sto_no(_df)
    _df = create_uid(df=_df, col1="temp", col2="item_description")
    new_col_list = [
        'uid', 'sto_no', 'item_description', 'receiving_plant',
        'delivery_no', 'pgi_date', 'pgi_quantity', 'pgi_uom'
    ]
    _df = _df[new_col_list]
    return _df


def create_uid(df: pd.DataFrame, col1: str, col2: str) -> pd.DataFrame:
    df = create_temp_sto_no(df)
    df["uid"] = df[col1] + " " + df[col2]
    df = df.drop("temp", axis=1)
    return df


def make_weekly_prod_df(df: pd.DataFrame) -> pd.DataFrame:
    _df = create_temp_sto_no(df)
    _df = create_uid(_df, "temp", "item")
    new_col_list = ["uid", "sto_no", "item", "quantity_kg", "production", "fg"]
    _df = _df[new_col_list]
    return _df


def merge_pgi_weekly(df1: pd.DataFrame, df2: pd.DataFrame, key: str, how: str):
    _df = df1.merge(df2, on=key, how=how)
    return _df


def has_gum_text(text: str):
    if "gum" in text.lower():
        return True
    return False


def make_summary_df(df: pd.DataFrame) -> pd.DataFrame:
    selected_columns = [
        "sto_no", "item_description",
        "receiving_plant", "sku_uom",
        "item_sku_qty", "pgi_quantity"
    ]
    _df = df[selected_columns]
    _df = _df[_df["sku_uom"] != "PC"]
    _df = _df[~df["item_description"].apply(lambda x: has_gum_text(x))]
    _df = create_uid(df=_df, col1="temp", col2="item_description")
    _df = (_df
           .groupby(["uid", "sto_no", "item_description", "receiving_plant", "sku_uom", "item_sku_qty"])
           .agg(pgi_quantity=("pgi_quantity", "sum"))
           .reset_index()
           )
    _df["pending_qty"] = _df["item_sku_qty"] - _df["pgi_quantity"]
    return _df.copy()



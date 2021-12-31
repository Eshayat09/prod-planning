from pathlib import Path
from prodplan.schema import COLUMN_SCHEMA, WEEKLY_PRD_SCHEMA, REQUIRED_COLUMNS, WEEKLY_RPD_REQUIRED_COLUMNS
import prodplan.dfops as ops

# Thant can be change every day
FILE_PATH = Path('data').joinpath('STO Report 01.09.21-19.12.21.XLSX')
WRITE_PATH = Path("data").joinpath("merged.XLSX")

RAW_DF = ops.read_to_dataframe(
    path=FILE_PATH,
    required_column=REQUIRED_COLUMNS,
    column_schema=COLUMN_SCHEMA,
    sheet_name="Sheet1"
)

WEEKLY_PROD = ops.read_weekly_prod(
    path=FILE_PATH,
    required_column=WEEKLY_RPD_REQUIRED_COLUMNS,
    column_schema=WEEKLY_PRD_SCHEMA,
    sheet_name="Weekly Prod. Sche. 12.12-18.12",
)


PGI_QTY_DF = ops.make_pgi_qty_df(RAW_DF)
WKL_DLV_DF = ops.make_weekly_prod_df(WEEKLY_PROD)
SUMMARY_DF = ops.make_summary_df(RAW_DF)

WKL_SUMM_MERGED = ops.merge_pgi_weekly(SUMMARY_DF, WKL_DLV_DF, "uid", "left")

WKL_SUMM_MERGED.to_excel(WRITE_PATH, index=False)


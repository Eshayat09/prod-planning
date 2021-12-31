REQUIRED_COLUMNS = [
    'STO No.', 'STO Status', 'Receiving Plant',
    'Item Description', 'Item SKU Qty', 'SKU UoM',
    'Delivery No', 'PGI Quantity', 'PGI UoM', 'PGI Date'
]

COLUMN_CLEANED = [item.lower().replace(" ", "_").replace(".", "").replace("/", "") for item in REQUIRED_COLUMNS]

COLUMN_SCHEMA = dict(zip(REQUIRED_COLUMNS, COLUMN_CLEANED))

WEEKLY_RPD_REQUIRED_COLUMNS = ['STO No.', 'Item', 'Quantity (kg)', 'Production', 'FG']

WEEKLY_RPD_REQUIRED_COLUMNS_CLEANED = [
    item.lower()
        .replace(" ", "_")
        .replace(".", "")
        .replace("/", "")
        .replace("(", "")
        .replace(")", "")

    for item in WEEKLY_RPD_REQUIRED_COLUMNS
]

WEEKLY_PRD_SCHEMA = dict(zip(WEEKLY_RPD_REQUIRED_COLUMNS, WEEKLY_RPD_REQUIRED_COLUMNS_CLEANED))
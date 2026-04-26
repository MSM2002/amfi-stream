import pyarrow as pa
import pyarrow.compute as pc

NULL_VARIANTS = ["", "-"]

SCHEME_MASTER_SCHEMA = pa.schema(
    [
        ("AMC", pa.string()),
        ("Code", pa.uint32()),
        ("Scheme Name", pa.string()),
        ("Scheme Type", pa.string()),
        ("Scheme Category", pa.string()),
        ("Scheme NAV Name", pa.string()),
        ("Scheme Minimum Amount", pa.string()),
        ("Launch Date", pa.date32()),
        ("Closure Date", pa.date32()),
        ("ISIN Div Payout/ ISIN GrowthISIN Div Reinvestment", pa.string()),
    ]
)

LATEST_NAV_SCHEMA = pa.schema(
    [
        ("Scheme Code", pa.uint32()),
        ("ISIN Div Payout/ ISIN Growth", pa.string()),
        ("ISIN Div Reinvestment", pa.string()),
        ("Scheme Name", pa.string()),
        ("Net Asset Value", pa.float64()),
        ("Date", pa.date32()),
    ]
)

MONTH_KEYS = pa.array(
    [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
)

MONTH_VALUES = pa.array(
    ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
)


def apply_null(col: pa.Array) -> pa.Array:
    mask = pc.is_in(col, pa.array(NULL_VARIANTS))
    return pc.if_else(mask, pa.scalar(None, type=col.type), col)


def parse_dmy_date(col: pa.Array) -> pa.Array:
    parts = pc.split_pattern(col, "-")

    day = pc.list_element(parts, 0)
    month = pc.list_element(parts, 1)
    year = pc.list_element(parts, 2)

    index = pc.index_in(month, value_set=MONTH_KEYS)
    month_number = pc.take(MONTH_VALUES, index)

    iso_date_string = pc.binary_join_element_wise(
        year, pc.binary_join_element_wise(month_number, day, "-"), "-"
    )

    return pc.strptime(iso_date_string, format="%Y-%m-%d", unit="s")


def cast_to(col, dtype):
    return pc.cast(col, dtype)


def normalise_column(col, field):
    if pa.types.is_string(col.type):
        col = pc.utf8_trim_whitespace(pc.cast(col, pa.string()))
        col = apply_null(col)

    if pa.types.is_date(field.type):
        col = parse_dmy_date(col)

    col = cast_to(col, field.type)

    return col


def trim_table_column_names(table: pa.Table) -> pa.Table:
    return table.rename_columns([name.strip() for name in table.column_names])


def normalise_table(table, schema):
    table = trim_table_column_names(table)
    arrays = []
    for field in schema:
        col = table[field.name]
        col = normalise_column(col, field)
        arrays.append(col)
    return pa.Table.from_arrays(arrays, schema=schema)


def normalise_scheme_master(table: pa.Table) -> pa.Table:
    table = normalise_table(table, SCHEME_MASTER_SCHEMA)
    return table


def normalise_latest_nav(table: pa.Table) -> pa.Table:
    table = normalise_table(table, LATEST_NAV_SCHEMA)
    return table

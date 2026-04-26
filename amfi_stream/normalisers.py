import pyarrow as pa
import pyarrow.compute as pc


def normalise_scheme_master(table: pa.Table) -> pa.Table:
    cols = table.column_names
    new_cols = []

    for col in cols:
        arr = table[col]

        if pa.types.is_string(arr.type):
            arr = pc.utf8_trim_whitespace(arr)

        new_cols.append(arr)

    return pa.Table.from_arrays(new_cols, names=cols)

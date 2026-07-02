import csv
import os
import numpy as np


def load_column(filepath, column_name):
    """
    Load a single numeric column from a CSV into a 1D NumPy array.
    Assumes the CSV has a header row.

    Strategy: read the header with Python's csv module to find the
    column index, then let genfromtxt load *only that column* as
    dtype=float.  This ensures missing values become NaN (not -1,
    which is what happens with dtype=None on integer-inferred columns).
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: '{filepath}'")

    # --- Pass 1: read just the header to resolve the column name ---
    with open(filepath, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)

    # Strip whitespace from header names for resilient matching
    header = [h.strip() for h in header]

    if column_name not in header:
        raise ValueError(
            f"Column '{column_name}' not found. "
            f"Available columns: {header}"
        )

    col_idx = header.index(column_name)

    # --- Pass 2: load the single column as float ---
    column = np.genfromtxt(
        filepath,
        delimiter=',',
        skip_header=1,            # we already read the header ourselves
        usecols=(col_idx,),       # load only the target column
        dtype=float,              # force float so blanks → NaN
        filling_values=np.nan,
        encoding='utf-8'
    )

    # Handle the case where the CSV has exactly one data row
    # (genfromtxt returns a 0-d array instead of 1-d)
    column = np.atleast_1d(column)

    # Drop NaN values explicitly rather than silently propagating them
    nan_mask = np.isnan(column)
    n_missing = int(np.sum(nan_mask))
    if n_missing > 0:
        print(f"Warning: {n_missing} missing value(s) dropped from '{column_name}'")
        column = column[~nan_mask]

    if len(column) == 0:
        raise ValueError(
            f"Column '{column_name}' has no valid numeric values after "
            f"removing {n_missing} missing entries."
        )

    return column
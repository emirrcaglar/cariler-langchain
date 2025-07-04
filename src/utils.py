def check_shrink_df(df, max_rows, std_condition=None):
    """Check DataFrame size and show sample if necessary."""
    row_count, col_count = df.shape
    if row_count > max_rows:
        df = df.head(max_rows)
        info = (
            f"DataFrame filtered by standardized condition '{std_condition}'.\n"
            f"Result has {row_count} rows and {col_count} cols. \n"
            f"{df.to_string()}"
        )
    else:
        info = (
            f"DataFrame filtered by standardized condition '{std_condition}'.\n"
            f"{df.to_string()}"
        )
    return df, info

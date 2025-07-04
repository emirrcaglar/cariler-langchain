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


import tiktoken
def count_tokens(messages, model="gpt-3.5-turbo"):
    enc = tiktoken.encoding_for_model(model)
    history = []
    total_tokens = 0
    for msg in messages:
        # If msg is a string, just encode it
        if isinstance(msg, str):
            total_tokens += len(enc.encode(msg))
            history.append(msg)
        # If msg is a LangChain message object, use its content
        elif hasattr(msg, "content"):
            total_tokens += len(enc.encode(msg.content))
            history.append(msg)
    return total_tokens, history
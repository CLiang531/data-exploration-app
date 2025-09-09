def pd_search_text(df, chosen_cols, search_keyword):
    if chosen_cols:
        for col in chosen_cols:
            df = df[
                df[col]
                .astype(str)
                .str.contains(search_keyword, case=False, regex=False, na=False)
            ]
    return df


def pd_search_num_range(df, chosen_cols, mn, mx):
    if chosen_cols:
        for col in chosen_cols:
            df = df[(df[col] >= mn) & (df[col] <= mx)]
    return df

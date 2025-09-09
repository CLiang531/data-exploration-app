import re

import pandas as pd


def summarize(df):
    info = pd.DataFrame(
        {
            "Type": df.dtypes,
            "Null": df.isnull().sum(),
            "% Null": [round(num / len(df), 2) for num in df.isnull().sum()],
            "Unique": [len(df[col].value_counts()) for col in df.columns],
        }
    )
    summary = {
        "Data Preview": df,
        "Summary": df.describe().T,
        "Basic Information": info,
    }
    return summary


def convert_id(df):
    pattern = re.compile(r"\bid\b", re.IGNORECASE)
    for col in df.columns:
        if bool(pattern.search(col)):
            df[col] = df[col].astype(str)

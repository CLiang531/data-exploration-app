import streamlit as st

from util_app.filters.pd_filters import pd_search_num_range, pd_search_text
from util_app.filters.sql_filters import sql_search_num_range, sql_search_text
from util_app.ui.dialogs import error_msg
from util_app.ui.st_helpers import MS_TYPE, TI_TYPE, generate_saved_input


def search_text(df, section_i, df_i, input_i=0):
    test_cols = df.select_dtypes(include=["object", "string"]).columns
    search_cols = []
    for col in test_cols:
        try:
            df.loc[:, col] = df[col].astype(str)
            search_cols.append(col)
        except:
            pass

    if len(search_cols) > 0:
        chosen_cols = None
        search_keyword = ""

        st.markdown("#### Search Text")
        col1, col2 = st.columns(2)
        with col1:
            chosen_cols, input_i = generate_saved_input(
                "Column:",
                MS_TYPE,
                section_i,
                input_i,
                subsection_i=df_i,
                options=search_cols,
            )
        with col2:
            search_keyword, input_i = generate_saved_input(
                "Search:", TI_TYPE, section_i, input_i, subsection_i=df_i
            )

        if chosen_cols:
            df = pd_search_text(df, chosen_cols, search_keyword)

    return df, input_i


def search_range(df, section_i, df_i, input_i=0):
    search_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(search_cols) > 0:
        chosen_cols = None
        search_min, search_max = float("-inf"), float("inf")

        st.markdown("#### Search Numbers")
        col1, col2, col3 = st.columns(3)
        with col1:
            chosen_cols, input_i = generate_saved_input(
                "Column:",
                MS_TYPE,
                section_i,
                input_i,
                subsection_i=df_i,
                options=search_cols,
            )
        with col2:
            min, input_i = generate_saved_input(
                "Min:", TI_TYPE, section_i, input_i, subsection_i=df_i
            )
            try:
                search_min = float(min)
            except:
                search_min = float("-inf")
        with col3:
            max, input_i = generate_saved_input(
                "Max:", TI_TYPE, section_i, input_i, subsection_i=df_i
            )
            try:
                search_max = float(max)
            except:
                search_max = float("inf")

        if chosen_cols:
            df = pd_search_num_range(df, chosen_cols, search_min, search_max)

    return df, input_i

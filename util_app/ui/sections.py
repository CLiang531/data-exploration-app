import streamlit as st

from project_utils.data_helpers import summarize
from util_app.ui.file_upload import upload
from util_app.ui.graphs import graph_chart
from util_app.ui.st_helpers import get_nxt_i
from util_app.utils.settings import settings
from util_app.ui.dataframe import show_df


def file_upload():
    st.subheader("Choose Dataset")

    section_i = "file_upload"
    if section_i not in st.session_state:
        st.session_state[section_i] = []

    df = upload(section_i)

    if df is not None:
        summary = summarize(df)
        df_section(summary)
        graph_section(df)


def df_section(summary):
    st.header("General Data Information")
    df_section_container = st.container()
    subheaders = list(summary.keys())
    dfs = list(summary.values())

    section_i = "df_options"
    if section_i not in st.session_state:
        st.session_state[section_i] = []
    get_nxt_i(section_i, section_len=len(dfs))

    with df_section_container:
        for i in range(len(dfs)):
            show_df(dfs[i], section_i, i, subheaders[i])


def graph_section(df):
    st.subheader("Graphs")
    graph_section_container = st.container()
    graph_containers = []

    section_i = "graph_options"
    if section_i not in st.session_state:
        st.session_state[section_i] = []
    st.button(
        "Graph",
        icon=":material/add:",
        use_container_width=True,
        key="add_btn",
        on_click=lambda: get_nxt_i(section_i),
    )

    with graph_section_container:
        for i in range(len(st.session_state[section_i])):
            graph_containers.append(st.container(border=True))
            with graph_containers[i]:
                graph_chart(df, section_i, i)

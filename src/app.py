import os
import sys

import streamlit as st

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../util_app/..")
)
from util_app.db.db_connection import db
from util_app.ui import sections
from util_app.ui.dialogs import error_msg
from util_app.utils.settings import settings


@st.cache_resource
def setup_sql():
    db.setup_connection()
    connected, msg = db.connect_status()
    if not connected:
        error_msg(
            "SQL Error",
            "Could not connect to SQL database; SQL will be disabled. If you would like to continue using SQL, please verify your credentials and try again.",
            msg,
        )


def app():
    title = "Data Analysis Tool"
    st.title(title)
    st.markdown(
        """
        <style>
        h1 svg, h2 svg, h3 svg, h4 svg {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    try:
        sql = settings.get_section("sql")["enabled"]
        if sql:
            setup_sql()
        st.set_page_config(page_title=title, page_icon=":bar_chart:", layout="wide")
        sections.file_upload()
    except KeyboardInterrupt:
        db.close_connection()


app()

import streamlit as st

from project_utils.read_data import kaggle_download, load_file
from util_app.db.db_connection import db
from util_app.db.sql_helpers import delete_tbl, select_all_tbl
from util_app.ui.dialogs import error_msg
from util_app.ui.st_helpers import SB_TYPE, TI_TYPE, generate_saved_input, get_nxt_i
from util_app.utils.settings import settings


@st.cache_data
def read_upload(file):
    return load_file(file)


@st.cache_data
def download_kaggle_dataset(download_link, input_folder):
    return kaggle_download(download_link, input_folder)


def upload(section_i):
    uploader = st.empty()
    kaggle_link = st.container()
    prev_uploads = st.container()

    df = None
    file_name = None
    file = None
    input_i = 0
    sql = settings.get_section("sql")["enabled"]

    if 'upload_cnt' not in st.session_state:
        st.session_state['upload_cnt'] = 0

    with uploader:
        key = 'upload_file' + str(st.session_state['upload_cnt'])
        file = st.file_uploader(
            "Upload CSV or Excel file:", type=["csv", "xlsx", "xls"], key = key
        )
    if file is not None:
        df = read_upload(file)
        file_name = file.name
        st.session_state['upload_cnt'] += 1

    with kaggle_link:
        desc = "On the Kaggle website, click the download button, choose 'download via kaggle', and then paste the dataset identifier located within kagglehub.dataset_download(\"dataset_identifier\")"
        download_link, input_i = generate_saved_input(
            "Kaggle Link", TI_TYPE, section_i, input_i, placeholder=desc
        )
        if download_link is not None and len(download_link) > 0:
            try:
                file_name, df = download_kaggle_dataset(download_link, settings.get_section('input_folder'))
                st.session_state[section_i][input_i - 1] = None
            except Exception as e:
                error_msg(
                    "Kaggle Upload Error",
                    "Failed to download file from Kaggle. Verify that the dataset identifier is accurate and try again.",
                    str(e),
                )

    if sql:
        if df is not None and file_name is not None:
            db.create_df_table(df, file_name)
        options = db.execute_query(select_all_tbl())
        options = [None] + [o[0] for o in options]
        if file_name is not None:
            get_nxt_i(section_i, input_i + 1)
            st.session_state[section_i][input_i] = file_name
        with prev_uploads:
            col1, col2 = st.columns([5, 1])
            with col1:
                file_name, input_i = generate_saved_input(
                    "Previously Uploaded Datasets",
                    SB_TYPE,
                    section_i,
                    input_i,
                    options=options,
                )
            with col2:
                st.markdown(
                    "<div style='height: 1.7em;'></div>", unsafe_allow_html=True
                )
                st.button(
                    "Delete",
                    use_container_width=True,
                    key="delete_btn",
                    on_click=lambda: db.execute_query(delete_tbl(file_name)),
                )
        if file_name is not None:
            df = db.select_df_table(file_name)

    return df

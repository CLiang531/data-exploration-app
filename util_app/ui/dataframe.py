import streamlit as st
from util_app.filters.filters import search_range, search_text
from util_app.utils.id_generator import generate_id

def display_df(df, df_placeholder):
    with df_placeholder:
        st.dataframe(df, column_config={"_index": st.column_config.Column(width=None)})


def download_df(df):
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.markdown(
        """
        <style>
        div.stDownloadButton > button {
            padding-top: 0rem;
            padding-bottom: 0rem;
            font-size: 1rem; /* match text size */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.download_button('Download', data=csv_data, file_name='result.csv', mime='text/csv', key=generate_id(), use_container_width=True)

def show_df(df, section_i, df_i, subheader):
    col1, col2 = st.columns([10, 1])
    with col1:
        st.subheader(subheader)
    with col2:
        download_df(df)
    df, input_i = search_range(df, section_i, df_i)
    df, input_i = search_text(df, section_i, df_i, input_i)
    df_display = st.empty()
    display_df(df, df_display)
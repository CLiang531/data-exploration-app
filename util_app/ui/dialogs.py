import streamlit as st


@st.dialog("Error")
def error_msg(error_type, msg, error_msg=None):
    error_desc = error_type + ": " + msg
    st.write(error_desc)
    if error_msg is not None:
        st.caption("\nError Message:")
        st.caption(error_msg)

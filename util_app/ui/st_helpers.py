import streamlit as st

from util_app.utils.id_generator import generate_id

SB_TYPE = "sb"
TI_TYPE = "ti"
MS_TYPE = "ms"


def in_list(value, search_list):
    if isinstance(value, list):
        return all(i in search_list for i in value)
    else:
        return value in search_list


def get_nxt_i(section_i, section_len=None):
    state = st.session_state[section_i]
    if section_len is not None:
        while len(state) < section_len:
            state.append([])
    else:
        state.append([])


def update_value(saved_options, input_i, key):
    if input_i < len(saved_options):
        saved_options[input_i] = st.session_state[key]
    else:
        saved_options.append(st.session_state[key])


def delete_input(section_i, subsection_i=None):
    if subsection_i is None:
        st.session_state.pop(section_i, None)
    else:
        st.session_state[section_i].pop(subsection_i)


def generate_saved_input(
    msg,
    input_type,
    section_i,
    input_i,
    subsection_i=None,
    options=None,
    placeholder=None,
):
    key = generate_id()
    saved_options = st.session_state[section_i]
    if subsection_i is not None:
        saved_options = saved_options[subsection_i]
    update = lambda: update_value(saved_options, input_i, key)

    valid_no_options = (options is None) and (input_type == TI_TYPE)

    if input_i < len(saved_options) and (
        valid_no_options
        or ((options is not None) and in_list(saved_options[input_i], options))
    ):
        if input_type == SB_TYPE:
            try:
                option = options.index(saved_options[input_i])
            except:
                option = None
            value = st.selectbox(
                msg,
                options=options,
                index=option,
                key=key,
                on_change=update,
            )
        elif input_type == TI_TYPE:
            value = st.text_input(
                msg,
                value=saved_options[input_i],
                key=key,
                on_change=update,
                placeholder=placeholder,
            )
        elif input_type == MS_TYPE:
            value = st.multiselect(
                msg,
                options=options,
                default=saved_options[input_i],
                key=key,
                on_change=update,
            )
    else:
        if input_type == SB_TYPE:
            if key not in st.session_state:
                st.session_state[key] = options[0]
            update_value(saved_options, input_i, key)
            value = st.selectbox(msg, options=options, key=key, on_change=update)
        elif input_type == TI_TYPE:
            if key not in st.session_state:
                st.session_state[key] = ""
            update_value(saved_options, input_i, key)
            value = st.text_input(
                msg, key=key, on_change=update, placeholder=placeholder
            )
        elif input_type == MS_TYPE:
            if key not in st.session_state:
                st.session_state[key] = []
            update_value(saved_options, input_i, key)
            value = st.multiselect(msg, options=options, key=key, on_change=update)

    return value, input_i + 1

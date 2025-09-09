import plotly.express as px
import streamlit as st

from util_app.ui.st_helpers import (SB_TYPE, TI_TYPE, delete_input,
                                    generate_id, generate_saved_input)


def heatmap(df, graph_placeholder):
    with graph_placeholder:
        axis_font_size = 16
        cell_font_size = 14
        df_clean = df.dropna(axis=1, how="all")
        fig = px.imshow(
            df_clean.corr(numeric_only=True),
            text_auto=".4f",
            aspect="auto",
            color_continuous_scale="inferno",
        )
        fig.update_layout(
            height=1200,
            width=800,
            font=dict(size=cell_font_size),
            xaxis_tickfont_size=axis_font_size,
            yaxis_tickfont_size=axis_font_size,
        )
        st.plotly_chart(fig, key=generate_id())


def pie_chart(df, graph_placeholder, col):
    with graph_placeholder:
        cnts = df[col].value_counts()
        names = cnts.index.to_list()
        values = cnts.values
        fig = px.pie(df, values=values, names=names, hole=0.4)
        font_size = 16
        fig.update_layout(
            height=600, width=600, font=dict(size=font_size), legend_font_size=font_size
        )
        st.plotly_chart(fig, key=generate_id())


def bar_chart(
    df, graph_placeholder, x_col, y_col="Count", color=None, stack=True, bins=0
):
    if bins > 0:
        col_name = x_col + " By " + str(bins) + "s"
        df[col_name] = (df[x_col] // bins) * bins
        x_col = col_name
    if y_col == "Count":
        cols = [x_col]
        if color:
            cols += [color]
        df = df.groupby(cols).size().reset_index(name="Count")
    with graph_placeholder:
        st.bar_chart(df, x=x_col, y=y_col, color=color, horizontal=True, stack=stack)
    if bins > 0:
        df.drop(columns=[col_name])


def line_chart(df, graph_placeholder, x_col, y_col, color=None):
    with graph_placeholder:
        st.line_chart(df, x=x_col, y=y_col, color=color)


def scatter_plot(df, graph_placeholder, x_col, y_col, color=None):
    with graph_placeholder:
        st.scatter_chart(df, x=x_col, y=y_col, color=color)


@st.fragment()
def graph_chart(df, section_i, graph_i):
    search_bar = st.empty()
    graph_placeholder = st.empty()

    graphs = ["Heatmap", "Pie Chart", "Bar Chart", "Line Chart", "Scatter Plot"]
    num_cols = df.select_dtypes(include=["int64", "float64"]).columns.to_list()
    color_options = [None] + df.columns.to_list()
    all_cols = df.columns.to_list()
    input_i = 0

    with search_bar:
        graph_type_col, x_col, y_col, choice_col_1, choice_col_2, choice_col_3 = (
            st.columns(6)
        )
        with graph_type_col:
            graph_type, input_i = generate_saved_input(
                "Graph Type:",
                SB_TYPE,
                section_i,
                input_i,
                subsection_i=graph_i,
                options=graphs,
            )
            if graph_type == graphs[0]:
                heatmap(df, graph_placeholder)
            elif graph_type == graphs[1]:
                with x_col:
                    col, input_i = generate_saved_input(
                        "Select a Column:",
                        SB_TYPE,
                        section_i,
                        input_i,
                        subsection_i=graph_i,
                        options=all_cols,
                    )
                    pie_chart(df, graph_placeholder, col)
            elif graph_type == graphs[2]:
                stack, bins = None, None
                bar_y_options = ["Count"] + num_cols
                stack_options = [True, False]
                with x_col:
                    x, input_i = generate_saved_input(
                        "Select x-axis:",
                        SB_TYPE,
                        section_i,
                        input_i,
                        subsection_i=graph_i,
                        options=all_cols,
                    )
                with y_col:
                    y, input_i = generate_saved_input(
                        "Select y-axis:",
                        SB_TYPE,
                        section_i,
                        input_i,
                        subsection_i=graph_i,
                        options=bar_y_options,
                    )
                with choice_col_1:
                    color, input_i = generate_saved_input(
                        "[OPTIONAL] Select Color-Coding Column:",
                        SB_TYPE,
                        section_i,
                        input_i,
                        subsection_i=graph_i,
                        options=color_options,
                    )
                with choice_col_2:
                    stack, input_i = generate_saved_input(
                        "[OPTIONAL WITH COLOR] Stack?",
                        SB_TYPE,
                        section_i,
                        input_i,
                        subsection_i=graph_i,
                        options=stack_options,
                    )
                with choice_col_3:
                    bins, input_i = generate_saved_input(
                        "[OPTIONAL] Bin Size (Positive #s Only):",
                        TI_TYPE,
                        section_i,
                        input_i,
                        subsection_i=graph_i,
                    )
                    try:
                        bins = int(bins)
                    except:
                        bins = 0
                bar_chart(df, graph_placeholder, x, y, color, stack, bins)
            else:
                x, y, color = None, None, None
                with x_col:
                    x, input_i = generate_saved_input(
                        "Select x-axis:",
                        SB_TYPE,
                        section_i,
                        input_i,
                        subsection_i=graph_i,
                        options=num_cols,
                    )
                with y_col:
                    y, input_i = generate_saved_input(
                        "Select y-axis:",
                        SB_TYPE,
                        section_i,
                        input_i,
                        subsection_i=graph_i,
                        options=num_cols,
                    )
                with choice_col_1:
                    color, input_i = generate_saved_input(
                        "[OPTIONAL] Select Color-Coding Column:",
                        SB_TYPE,
                        section_i,
                        input_i,
                        subsection_i=graph_i,
                        options=color_options,
                    )
                if graph_type == graphs[3]:
                    line_chart(df, graph_placeholder, x, y, color)
                elif graph_type == graphs[4]:
                    scatter_plot(df, graph_placeholder, x, y, color)

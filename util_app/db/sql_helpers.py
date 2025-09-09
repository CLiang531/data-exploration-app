def create_db(dbname):
    return f"CREATE DATABASE {dbname}"


def select_all_tbl():
    return (
        "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    )


def select_tbl(df_name):
    return f'SELECT * FROM "{df_name}"'


def delete_tbl(df_name):
    return f'DROP TABLE "{df_name}"'


# ===================================================
# SQL helper functions for future use
# Currently not used in the main app
# ===================================================


def insert_row(tbl_name, col_names, col_values):
    query = f"INSERT INTO {tbl_name} ("
    for i in range(len(col_names)):
        query += col_names[i]
        if i == len(col_names[i]) - 1:
            query += ", "
    query += ") VALUES ("
    for i in range(len(col_values)):
        query += col_values[i]
        if i == len(col_values[i]) - 1:
            query += ", "
    query += ")"


def create_tbl(tbl_name, col_names, data_types):
    query = f"CREATE TABLE {tbl_name} ("
    for i in range(len(col_names)):
        query += f"{col_names[i]} {data_types[i]}"
        if i == len(col_names[i]) - 1:
            query += ", "
    query += ")"


def search_text(df_name, cols, keyword):
    query = f"SELECT * FROM {df_name}"
    if len(keyword) > 0:
        query += " WHERE "
        for i in range(len(cols)):
            query += f"{cols[i]} LIKE '%{keyword}%'"
            if i == len(cols) - 1:
                query += " AND "
    return query


def search_num_range(df_name, cols, mn, mx):
    query = f"SELECT * FROM {df_name}"
    if mn is not float("-inf") or mx is not float("inf"):
        query += " WHERE "
        for i in range(len(cols)):
            if mn is not float("-inf") and mx is not float("inf"):
                query += f"({cols[i]} BETWEEN {mn} AND {mx})"
            elif mn is not float("-inf"):
                query += f"({cols[i]} <= {mn})"
            elif mx is not float("inf"):
                query += f"({cols[i]} >= {mn})"
            if i == len(cols) - 1:
                query += " AND "
    return query

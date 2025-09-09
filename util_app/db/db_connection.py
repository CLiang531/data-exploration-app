import pandas as pd
import psycopg2
from sqlalchemy import create_engine

from util_app.db.sql_helpers import select_tbl
from util_app.utils.settings import settings


class DBConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.engine = None
        self.connected = False
        self.error_msg = "Connection not set up."

    def setup_connection(self):
        try:
            credentials = settings.get_section("sql")

            self.conn = psycopg2.connect(
                dbname="postgres",
                user=credentials["user"],
                password=credentials["password"],
                host=credentials["host"],
                port=credentials["port"],
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()

            self.cursor.execute(
                f"SELECT datname FROM pg_database WHERE datname='{credentials['dbname']}'"
            )
            row = self.cursor.fetchone()
            if row is None:

                self.cursor.execute(f"CREATE DATABASE {credentials['dbname']}")

            self.conn = psycopg2.connect(
                dbname=credentials["dbname"],
                user=credentials["user"],
                password=credentials["password"],
                host=credentials["host"],
                port=credentials["port"],
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()

            encoded_pw = credentials["password"].replace("@", "%40").replace(":", "%3A")
            login = f"postgresql+psycopg2://{credentials['user']}:{encoded_pw}@{credentials['host']}:{credentials['port']}/{credentials['dbname']}"
            self.engine = create_engine(login)
            self.connected = True
            self.error_msg = None
        except Exception as e:
            settings.disable("sql")
            self.conn = None
            self.cursor = None
            self.engine = None
            self.error_msg = str(e)

    def connect_status(self):
        return self.connected, self.error_msg

    def execute_query(self, query):
        self.cursor.execute(query)
        try:
            return self.cursor.fetchall()
        except:
            return None

    def execute_df_query(self, query):
        return pd.read_sql_query(query, self.engine)

    def create_df_table(self, df, df_name):
        df.to_sql(
            df_name, con=self.engine, if_exists="replace", index=False, schema="public"
        )

    def select_df_table(self, df_name):
        query = select_tbl(df_name)
        return self.execute_df_query(query)

    def close_connection(self):
        if self.conn is not None:
            self.conn.close()
        if self.cursor is not None:
            self.cursor.close()
        if self.engine is not None:
            self.engine.dispose()


db = DBConnection()

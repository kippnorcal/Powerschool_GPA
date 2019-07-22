from os import getenv
import urllib
import pandas as pd
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text


class Connection:
    def __init__(self, schema="custom"):
        ip = getenv("SERVER_IP")
        db = getenv("DB")
        user = getenv("USER")
        pwd = getenv("PWD")
        driver = f"{{{pyodbc.drivers()[0]}}}"
        params = urllib.parse.quote_plus(
            f"DRIVER={driver};SERVER={ip};DATABASE={db};UID={user};PWD={pwd}"
        )
        self.schema = schema
        self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    def insert_into(self, table, df):
        df.to_sql(
            table, self.engine, schema=self.schema, if_exists="replace", index=True
        )


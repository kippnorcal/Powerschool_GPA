import glob
import os
import time
import logging
import sys
import traceback

import pandas as pd
from sqlsorcery import MSSQL

from browser import BrowserSession
import data_map
from mailer import notify


logging.basicConfig(
    filename="app.log",
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S%p",
)


def remove_old_files():
    export_files = glob.glob("student.export*")
    if len(export_files) > 0:
        for export_file in export_files:
            os.remove(export_file)


def create_df(filename):
    """Read CSV file into a pandas dataframe"""
    df = pd.read_csv(filename, sep="\t")
    df.rename(columns=data_map.column_names, inplace=True)
    return df


def read_logs(filename):
    """Read log messages for sending via email"""
    with open(filename) as f:
        return f.read()


def insert_table(df, tablename):
    """Drop and replace database table with each run"""
    df_len = len(df.index)
    sql = MSSQL()
    sql.insert_into(tablename, df, if_exists="replace")
    logging.info(f"Loaded {df_len} students into {tablename} table")


def main():
    try:
        remove_old_files()

        with BrowserSession() as b:
            b.search_students()
            b.quick_export_gpa()

        df = create_df("student.export.text")
        insert_table(df, "PS_GPA")

        success_message = read_logs("app.log")
        notify(success_message=success_message)
    except Exception as e:
        logging.error(e)
        stack_trace = traceback.format_exc()
        log_info = read_logs("app.log")
        error_message = f"{log_info}\n\n{stack_trace}"
        notify(error=True, error_message=error_message)


if __name__ == "__main__":
    main()

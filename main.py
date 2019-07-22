import argparse
import os
import pandas as pd
from db import Connection


parser = argparse.ArgumentParser()
parser.add_argument("--filepath", help="file path of csv to parse")
parser.add_argument("--tablename", help="name of the destination sql able")
args = parser.parse_args()
file = args.filepath
table = args.tablename

df = pd.read_csv(file, sep=",")
conn = Connection()
conn.insert_into("PS_GPA", df)
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
DB_PATH = BASE_DIR / "database" / "hospital.db"

conn = sqlite3.connect(DB_PATH)
print("Connected Successfully!")

admissions = pd.read_csv(DATA_DIR / "admissions.csv")
patients = pd.read_csv(DATA_DIR / "patients.csv")
diagnoses = pd.read_csv(DATA_DIR / "diagnoses.csv")
billing = pd.read_csv(DATA_DIR / "billing.csv")
hospitals = pd.read_csv(DATA_DIR / "hospitals.csv")

admissions.to_sql(
    "admissions",
    conn,
    if_exists="replace",
    index=False
)

patients.to_sql(
    "patients",
    conn,
    if_exists="replace",
    index=False
)

diagnoses.to_sql(
    "diagnoses",
    conn,
    if_exists="replace",
    index=False
)

billing.to_sql(
    "billing",
    conn,
    if_exists="replace",
    index=False
)

hospitals.to_sql(
    "hospitals",
    conn,
    if_exists="replace",
    index=False
)

tables = pd.read_sql(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table';
    """,
    conn
)

print(tables)

for table in tables["name"]:

    query = f"SELECT COUNT(*) AS rows FROM {table}"

    count = pd.read_sql(query, conn)

    print(table)

    print(count)

    print("-"*40)

conn.close()

print("Database Created Successfully!")
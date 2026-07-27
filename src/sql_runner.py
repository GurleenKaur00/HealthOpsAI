import sqlite3
from pathlib import Path
import pandas as pd

# ============================================================
# Project Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "hospital.db"
SQL_DIR = BASE_DIR / "sql"

# ============================================================
# Connect Database
# ============================================================

conn = sqlite3.connect(DB_PATH)

print("=" * 80)
print("Connected to SQLite Database")
print("=" * 80)

# ============================================================
# Check Database Tables
# ============================================================

tables = pd.read_sql_query(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table';
    """,
    conn
)

print("\nTables in Database:")
print(tables)

print("\n" + "=" * 80)


# ============================================================
# Execute SQL File
# ============================================================

def execute_sql_file(filename):

    file_path = SQL_DIR / filename

    print(f"\nExecuting File : {filename}")
    print("-" * 80)

    print("Full Path :", file_path)
    print("Exists    :", file_path.exists())

    if not file_path.exists():
        return

    # Read file
    with open(file_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    print("\nFile Size:", len(sql_script), "characters")
    print("Semicolons Found:", sql_script.count(";"))

    print("\nFirst 250 characters:\n")
    print(repr(sql_script[:250]))

    # Split statements
    statements = []

    for statement in sql_script.split(";"):

        statement = statement.strip()

        if statement != "":
            statements.append(statement)

    print("\nTotal SQL Statements Found:", len(statements))

    # Execute each query
    for i, statement in enumerate(statements, start=1):

        print("\n" + "=" * 80)
        print(f"Query {i}")
        print("=" * 80)

        print(statement[:120])
        print()

        try:

            df = pd.read_sql_query(statement, conn)

            print(df)

        except Exception as e:

            print("ERROR")
            print(e)

    print("\nFinished:", filename)
    print("=" * 80)


# ============================================================
# Execute All SQL Files
# ============================================================

sql_files = [
    "01_basic_queries.sql",
    "02_business_queries.sql",
    "03_advanced_queries.sql"
]

for file in sql_files:

    execute_sql_file(file)

# ============================================================
# Close Database
# ============================================================

conn.close()

print("\nAll SQL Files Executed Successfully!")

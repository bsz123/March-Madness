import sqlite3
import pandas as pd

def create_connection(db_file: str):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        team TEXT NOT NULL,
        assists REAL,
        fg_percent REAL,
        wins INTEGER,
        points INTEGER,
        rebounds INTEGER,
        blocks INTEGER,
        turnovers INTEGER
    );
    """
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()

def insert_data(conn, data: pd.DataFrame):
    insert_sql = """
    INSERT INTO stats (team, assists, fg_percent, wins, points, rebounds, blocks, turnovers)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    cursor = conn.cursor()
    for index, row in data.iterrows():
        cursor.execute(insert_sql, (row['Team'], row['assists'], row['fg_percent'], row['wins'],
                                     row['points'], row['rebounds'], row['blocks'], row['turnovers']))
    conn.commit()

def setup_database(db_file: str, excel_files: list):
    conn = create_connection(db_file)
    create_table(conn)

    combined_data = pd.DataFrame()
    for file in excel_files:
        df = pd.read_excel(file, sheet_name="Sheet1")
        combined_data = pd.concat([combined_data, df], ignore_index=True)

    insert_data(conn, combined_data)
    conn.close()

if __name__ == "__main__":
    excel_files = [
        "NCAA-data/assists.xlsx",
        "NCAA-data/fg-percent.xlsx",
        # Add paths for other Excel files as needed
    ]
    setup_database("NCAA_stats.db", excel_files)
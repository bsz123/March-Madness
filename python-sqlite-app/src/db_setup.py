import pandas as pd
import sqlite3
import os

def create_database(db_name: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_name)
    return conn

def create_tables(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS assists')
    cursor.execute('DROP TABLE IF EXISTS fg_percent')
    cursor.execute('DROP TABLE IF EXISTS teams')

    cursor.execute('''
        CREATE TABLE assists (
            Rank INTEGER,
            Team TEXT PRIMARY KEY,
            Assists INTEGER,
            Assists_Per_Game REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fg_percent (
            Rank INTEGER,
            Team TEXT PRIMARY KEY,
            FG_Percent REAL,
            FG_Made INTEGER,
            FG_Attempted INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            Team TEXT PRIMARY KEY,
            GM INTEGER,
            Wins INTEGER,
            Losses INTEGER,
            Win_Percentage REAL
        )
    ''')
    # Add more tables as needed for wins, points, rebounds, blocks, turnovers, etc.
    conn.commit()

def insert_data_from_csv(conn: sqlite3.Connection) -> None:
        # Define a custom method to use "INSERT OR IGNORE"
    def insert_or_ignore(table, conn, keys, data_iter):
        table_name = table if isinstance(table, str) else table.name
        placeholders = ", ".join(["?"] * len(keys))
        sql = f"INSERT OR IGNORE INTO {table_name} ({', '.join(keys)}) VALUES ({placeholders})"
        return conn.executemany(sql, data_iter)

    def parse_win_loss(wl: str) -> str:
        return wl.split("-")

    assists_df = pd.read_csv("NCAA-data/assists.csv")
    fg_df = pd.read_csv("NCAA-data/fg-percent.csv")


    teams_df = assists_df[['Team', 'GM', 'W-L']].drop_duplicates()
    teams_df[['Wins', 'Losses']] = teams_df['W-L'].str.split('-', expand=True).astype(int)
    teams_df.drop(columns=['W-L'], inplace=True)
    teams_df['Win_Percentage'] = (teams_df['Wins'] / teams_df['GM']).round(2)
    teams_df.to_sql('teams', conn, if_exists='append', index=False, method=insert_or_ignore)

    assists_table_df = assists_df.drop(columns=['GM', 'W-L']).rename(columns={'APG': 'Assists_Per_Game', 'AST': 'Assists'})
    fg_table_df = fg_df.drop(columns=['GM', 'W-L']).rename(columns={'FG%': 'FG_Percent', 'FGM': 'FG_Made', 'FGA': 'FG_Attempted'})

    assists_table_df.to_sql('assists', conn, if_exists='append', index=False)
    fg_table_df.to_sql('fg_percent', conn, if_exists='append', index=False)
    # Repeat for other dataframes

def main() -> None:
    db_name = "NCAA_data.db"
    conn = create_database(db_name)
    create_tables(conn)
    insert_data_from_csv(conn)
    conn.close()

if __name__ == "__main__":
    main()
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
    cursor.execute('DROP TABLE IF EXISTS assist_turnover_ratio')
    cursor.execute('DROP TABLE IF EXISTS blocks')
    cursor.execute('DROP TABLE IF EXISTS steals')
    cursor.execute('DROP TABLE IF EXISTS points_offense')
    cursor.execute('DROP TABLE IF EXISTS points_defense')
    cursor.execute('DROP TABLE IF EXISTS rebounds')
    cursor.execute('DROP TABLE IF EXISTS free_throw_percent')
    cursor.execute('DROP TABLE IF EXISTS team_colors')
    # Add more DROP TABLE statements as needed for other tables
    conn.commit()

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
    # AST	TO	Ratio
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assist_turnover_ratio (
            Rank INTEGER,
            Team TEXT PRIMARY KEY,
            Assist_Turnover_Ratio REAL,
            Assists INTEGER,
            Turnovers INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocks (
            Rank INTEGER,
            Team TEXT PRIMARY KEY,
            Blocks INTEGER,
            Blocks_Per_Game REAL
        )
    ''')
    # ORebs	DRebs	REB	RPG
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rebounds (
            Rank INTEGER,
            Team TEXT PRIMARY KEY,
            Offensive_Rebounds INTEGER,
            Defensive_Rebounds INTEGER,
            Total_Rebounds INTEGER,
            Rebounds_Per_Game REAL
        )
    ''')
    # ST	STPG
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS steals (
            Rank INTEGER,
            Team TEXT PRIMARY KEY,
            Steals INTEGER,
            Steals_Per_Game REAL
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS team_colors (
            Team TEXT PRIMARY KEY,
            Priamry_Color_Hex_Code TEXT,
            Secondary_Color_Hex_Code TEXT,
            Tertiary_Color_Hex_Code TEXT
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
    assist_turnover_ratio_df = pd.read_csv("NCAA-data/assist-turnover-ratio.csv")
    blocks_df = pd.read_csv("NCAA-data/blocks.csv")
    steals_df = pd.read_csv("NCAA-data/steals.csv")
    points_offense_df = pd.read_csv("NCAA-data/points-offense.csv")
    points_defense_df = pd.read_csv("NCAA-data/points-defense.csv")
    rebounds_df = pd.read_csv("NCAA-data/rebounds.csv")
    free_throw_df = pd.read_csv("NCAA-data/free-throw-percent.csv")

    team_colors_df = pd.read_csv("NCAA-data/color_teams.csv")

    teams_df = assists_df[['Team', 'GM', 'W-L']].drop_duplicates()

    teams_df[['Wins', 'Losses']] = teams_df['W-L'].str.split('-', expand=True).astype(int)
    teams_df.drop(columns=['W-L'], inplace=True)

    teams_df['Win_Percentage'] = (teams_df['Wins'] / teams_df['GM']).round(2)
    teams_df.to_sql('teams', conn, if_exists='append', index=False, method=insert_or_ignore)

    assists_table_df, fg_table_df, assist_turnover_ratio_table_df, blocks_table_df, steals_table_df, points_offense_table_df, points_defense_table_df, rebounds_table_df, free_throw_table_df = normalize_stats_dfs(assists_df, fg_df, assist_turnover_ratio_df, blocks_df, steals_df, points_offense_df, points_defense_df, rebounds_df, free_throw_df)

    team_colors_table_df = extract_team_colors(team_colors_df)

    save_stats_to_db(conn, insert_or_ignore, assists_table_df, fg_table_df, assist_turnover_ratio_table_df, blocks_table_df, steals_table_df, points_offense_table_df, points_defense_table_df, rebounds_table_df, free_throw_table_df, team_colors_table_df)

def normalize_stats_dfs(assists_df, fg_df, assist_turnover_ratio_df, blocks_df, steals_df, points_offense_df, points_defense_df, rebounds_df, free_throw_df):
    assists_table_df = assists_df.drop(columns=['GM', 'W-L']).rename(columns={'APG': 'Assists_Per_Game', 'AST': 'Assists'})
    fg_table_df = fg_df.drop(columns=['GM', 'W-L']).rename(columns={'FG%': 'FG_Percent', 'FGM': 'FG_Made', 'FGA': 'FG_Attempted'})
    # AST	TO	Ratio
    assist_turnover_ratio_table_df = assist_turnover_ratio_df.drop(columns=['GM', 'W-L', 'TO', 'AST']).rename(columns={'Ratio': 'Assist_Turnover_Ratio'}).drop_duplicates(subset=["Team"])
    # BLKS	BKPG
    blocks_table_df = blocks_df.drop(columns=['GM', 'W-L']).rename(columns={'BLKS': 'Blocks', 'BKPG': 'Blocks_Per_Game'})
    # ST	STPG
    steals_table_df = steals_df.drop(columns=['GM', 'W-L']).rename(columns={'ST': 'Steals', 'STPG': 'Steals_Per_Game'})
    points_offense_table_df = points_offense_df.drop(columns=['GM', 'W-L'])
    points_defense_table_df = points_defense_df.drop(columns=['GM', 'W-L'])
    rebounds_table_df = rebounds_df.drop(columns=['GM']).rename(columns={'ORebs': 'Offensive_Rebounds', 'DRebs': 'Defensive_Rebounds', 'REB': 'Total_Rebounds', 'RPG': 'Rebounds_Per_Game'})
    free_throw_table_df = free_throw_df.drop(columns=['GM', 'W-L'])
    return assists_table_df,fg_table_df,assist_turnover_ratio_table_df,blocks_table_df,steals_table_df,points_offense_table_df,points_defense_table_df,rebounds_table_df,free_throw_table_df

def extract_team_colors(team_colors_df):
    primary_color_df = team_colors_df.loc[team_colors_df['color_level'] == 1, ['Team', 'Hex_Code']] \
        .rename(columns={'Hex_Code': 'Priamry_Color_Hex_Code'})
    secondary_color_df = team_colors_df.loc[team_colors_df['color_level'] == 2, ['Team', 'Hex_Code']] \
        .rename(columns={'Hex_Code': 'Secondary_Color_Hex_Code'})
    tertiary_color_df = team_colors_df.loc[team_colors_df['color_level'] == 3, ['Team', 'Hex_Code']] \
        .rename(columns={'Hex_Code': 'Tertiary_Color_Hex_Code'})

    team_colors_table_df = primary_color_df.merge(secondary_color_df, on='Team').merge(tertiary_color_df, on='Team')
    return team_colors_table_df

def save_stats_to_db(conn, insert_or_ignore, assists_table_df, fg_table_df, assist_turnover_ratio_table_df, blocks_table_df, steals_table_df, points_offense_table_df, points_defense_table_df, rebounds_table_df, free_throw_table_df, team_colors_table_df):
    assists_table_df.to_sql('assists', conn, if_exists='append', index=False)
    fg_table_df.to_sql('fg_percent', conn, if_exists='append', index=False)
    assist_turnover_ratio_table_df.to_sql('assist_turnover_ratio', conn, if_exists='append', index=False, method=insert_or_ignore)
    blocks_table_df.to_sql('blocks', conn, if_exists='append', index=False, method=insert_or_ignore)
    steals_table_df.to_sql('steals', conn, if_exists='append', index=False)
    points_offense_table_df.to_sql('points_offense', conn, if_exists='append', index=False)
    points_defense_table_df.to_sql('points_defense', conn, if_exists='append', index=False)
    rebounds_table_df.to_sql('rebounds', conn, if_exists='append', index=False)
    free_throw_table_df.to_sql('free_throw_percent', conn, if_exists='append', index=False)
    team_colors_table_df.to_sql('team_colors', conn, if_exists='append', index=False)

def main() -> None:
    db_name = "NCAA_data.db"
    conn = create_database(db_name)
    create_tables(conn)
    insert_data_from_csv(conn)
    conn.close()

if __name__ == "__main__":
    main()
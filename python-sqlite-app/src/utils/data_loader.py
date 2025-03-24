import pandas as pd
import os

def load_excel_data(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    df = pd.read_excel(file_path, sheet_name="Sheet1", index_col=1)
    return df

def load_all_data() -> pd.DataFrame:
    assists_df = load_excel_data("NCAA-data/assists.xlsx")
    fg_df = load_excel_data("NCAA-data/fg-percent.xlsx")
    assist_turnover_ratio_df = load_excel_data("NCAA-data/assist-turnover-ratio.xlsx")
    blocks_df = load_excel_data("NCAA-data/blocks.xlsx")
    steals_df = load_excel_data("NCAA-data/steals.xlsx")
    points_offense_df = load_excel_data("NCAA-data/points-offense.xlsx")
    points_defense_df = load_excel_data("NCAA-data/points-defense.xlsx")
    rebounds_df = load_excel_data("NCAA-data/rebounds.xlsx")
    # Load additional data as needed
    # Example: wins_df = load_excel_data("NCAA-data/wins.xlsx")
    
    df = assists_df.merge(fg_df, on="Team")
    df = df.merge(assist_turnover_ratio_df, on="Team")
    df = df.merge(blocks_df, on="Team")
    df = df.merge(steals_df, on="Team")
    df = df.merge(points_offense_df, on="Team")
    df = df.merge(points_defense_df, on="Team")
    df = df.merge(rebounds_df, on="Team")

    # Merge additional dataframes as needed
    return df
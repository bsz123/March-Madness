import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3


def get_db_connection(db_path: str = "NCAA_data.db") -> sqlite3.Connection:
  return sqlite3.connect(db_path)


def query_table(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql_query(query, conn)


def displayChart(df: pd.DataFrame, x_axis: str, y_axis: str) -> None:
    st.title("NCAA Basketball Team Stats")

    fig = px.scatter(df, x=x_axis, y=y_axis, hover_name="Team",
                     title=f"Scatter Plot: {x_axis} vs {y_axis}")

    st.plotly_chart(fig)

def main():
    conn = get_db_connection()
    
    # Get common team data
    teams_df = query_table(conn, "teams")
    
    # Let the user select which tables supply the metric for each axis.
    metric_options = ["assists", "fg_percent"]
    x_metric = st.selectbox("Select metric table for X-axis", metric_options)
    y_metric = st.selectbox("Select metric table for Y-axis", metric_options, index=1)
    
    # Query both metric tables.
    x_df = query_table(conn, x_metric)
    y_df = query_table(conn, y_metric)
    
    # Merge teams info with metric data on 'Team'
    # (Assuming each metric table has a numeric metric column besides "Team")
    x_merged = pd.merge(teams_df, x_df, on="Team", how="inner")
    y_merged = pd.merge(teams_df, y_df, on="Team", how="inner")
    
    # Helper: get the numeric metric column name (ignoring 'Team', 'GM', 'WL')
    def get_metric_column(df):
        return next((col for col in df.columns if col not in ["Team", "GM", "WL"]), None)
    
    x_metric_col = get_metric_column(x_merged)
    y_metric_col = get_metric_column(y_merged)
    
    # Combine the metric values into one dataframe, keyed by Team.
    # We assume that both merged DataFrames have the same teams.
    combined_df = pd.merge(x_merged[["Team", x_metric_col]], 
                           y_merged[["Team", y_metric_col]], 
                           on="Team",
                           suffixes=("_x", "_y"))

    # Adjust the x and y column names to match the merged DataFrame
    new_x_metric_col = f"{x_metric_col}_x"
    new_y_metric_col = f"{y_metric_col}_y"

    
    displayChart(combined_df, new_x_metric_col, new_y_metric_col)
    
    conn.close()
    st.write("Done")
    print("Done")

main()
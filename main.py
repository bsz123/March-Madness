import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3


def get_db_connection(db_path: str = "NCAA_data.db") -> sqlite3.Connection:
  return sqlite3.connect(db_path)


def query_table(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql_query(query, conn)


def displayChart(df: pd.DataFrame, x_axis: str, y_axis: str, x_axis_options, y_axis_options ) -> None:
    st.title("NCAA Basketball Team Stats")
    stats = df.columns
    axis_options = [stat for stat in stats if stat not in ["Team", "GM", "WL"]]

    print(axis_options)
    def base_name(col_name: str) -> str:
        return col_name[:-2] if (col_name.endswith("_x") or col_name.endswith("_y")) else col_name

    x_axis_options = [
        col for col in df.columns
        if base_name(col) in x_axis_options and col not in ["Team", "GM", "WL", "Rank"]
    ]

    y_axis_options = [
        col for col in df.columns
        if base_name(col) in y_axis_options and col not in ["Team", "GM", "WL", "Rank"]
    ]

    print("Adjusted x_axis_options:", x_axis_options)
    
    x_axis = st.selectbox("Select X-axis", x_axis_options)
    y_axis = st.selectbox("Select Y-axis", y_axis_options)

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


    x_axis_options = [col for col in x_df.columns if col not in ["Team", "GM", "WL"]]
    y_axis_options = [col for col in y_df.columns if col not in ["Team", "GM", "WL"]]

    
    combined_df = pd.merge( x_df, y_df, on="Team")

    
    displayChart(combined_df, x_metric, x_metric, x_axis_options, y_axis_options)
    
    conn.close()
    st.write("Done")
    print("Done")

main()
import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3


def get_db_connection(db_path: str = "NCAA_data.db") -> sqlite3.Connection:
  return sqlite3.connect(db_path)


def query_table(conn: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql_query(query, conn)


def displayChart(df: pd.DataFrame) -> None:
    st.title("NCAA Basketball Team Stats")
    stats = df.columns
    axis_options = [stat for stat in stats]
    x_axis = st.selectbox("Select X-axis", axis_options)
    y_axis = st.selectbox("Select Y-axis", axis_options)

    fig = px.scatter(df, x=x_axis, y=y_axis, hover_name="Team",
                     title=f"Scatter Plot: {x_axis} vs {y_axis}")

    st.plotly_chart(fig)

def main():
    conn = get_db_connection()

    table_options = ["assists", "fg_percent"]
    selected_table = st.selectbox("Select table", table_options)

    df = query_table(conn, selected_table)
    teams_df = query_table(conn, "teams")
    df_with_team_record = pd.merge(df, teams_df, on="Team")

    displayChart(df_with_team_record)

    conn.close()
    st.write("Done")
    print("Done")

main()
import streamlit as st
import plotly.express as px

st.title("Test Plot in Streamlit")

fig = px.scatter(x=[1, 2, 3], y=[4, 5, 6])
st.plotly_chart(fig)
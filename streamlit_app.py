import streamlit as st
import pandas as pd 
import altair as alt 
import plotly.express as px

df = pd.read_csv('Data/movie_ratings.csv')

print(df.info())
print(df.describe())
print(df.head())

st.set_page_config(
    page_title="Movie Ratings Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)
alt.themes.enable("dark")


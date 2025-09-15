import streamlit as st
import pandas as pd 
import altair as alt 
import plotly.express as px

df = pd.read_csv('Data/movie_ratings.csv')

st.set_page_config(
    page_title="Movie Ratings Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)
alt.themes.enable("dark")

with st.sidebar:
    st.header('Filters')

    age_range = st.slider(
        'Select Age Range:',
        min_value=int(df['age'].min()),
        max_value=int(df['age'].max()),
        value=(int(df['age'].min()), int(df['age'].max()))
    )
    
    all_movies = sorted(df['title'].unique())
    selected_movies = st.multiselect(
        'Select Movies:',
        options=all_movies,
        default=all_movies
    )
    
    all_occupations = ['All'] + sorted(df['occupation'].unique())
    selected_occupation = st.selectbox(
        'Select Occupation:',
        options=all_occupations,
        index=0
    )
    
    all_genres = sorted(df['genres'].str.split('|').explode().unique())
    selected_genres = st.multiselect(
        'Select Genres:',
        options=all_genres,
        default=all_genres
    )


filtered_df = df[
    (df['age'] >= age_range[0]) & 
    (df['age'] <= age_range[1])
]


if selected_movies:
    filtered_df = filtered_df[filtered_df['title'].isin(selected_movies)]


if selected_occupation != 'All':
    filtered_df = filtered_df[filtered_df['occupation'] == selected_occupation]

if selected_genres:
    filtered_df = filtered_df[
        filtered_df['genres'].apply(
            lambda x: any(genre in x.split('|') for genre in selected_genres)
        )
    ]

st.header("Filtered Data Summary")
st.write(f"Total Movies in Filtered Data: **{filtered_df['movie_id'].nunique()}**")
st.write(f"Total Ratings in Filtered Data: **{len(filtered_df)}**")
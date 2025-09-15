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
    
    all_movies = ['All'] + sorted(df['title'].unique())
    selected_movie = st.selectbox(
        'Select a Movie:',
        options=all_movies,
        index=0
    )
    
    all_occupations = ['All'] + sorted(df['occupation'].unique())
    selected_occupation = st.selectbox(
        'Select Occupation:',
        options=all_occupations,
        index=0
    )
    
    all_genres = ['All'] + sorted(df['genres'].str.split('|').explode().unique())
    selected_genre = st.selectbox(
        'Select a Genre:',
        options=all_genres,
        index=0
    )


filtered_df = df[
    (df['age'] >= age_range[0]) & 
    (df['age'] <= age_range[1])
]


if selected_movie:
    filtered_df = filtered_df[filtered_df['title'].isin(selected_movie)]


if selected_occupation != 'All':
    filtered_df = filtered_df[filtered_df['occupation'] == selected_occupation]

if selected_genre:
    filtered_df = filtered_df[
        filtered_df['genres'].apply(
            lambda x: any(genre in x.split('|') for genre in selected_genre)
        )
    ]

st.header("Filtered Data Summary")
st.write(f"Total Movies in Filtered Data: **{filtered_df['movie_id'].nunique()}**")
st.write(f"Total Ratings in Filtered Data: **{len(filtered_df)}**")
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


if selected_movie != 'All':
    filtered_df = filtered_df[filtered_df['title'] == selected_movie]

if selected_occupation != 'All':
    filtered_df = filtered_df[filtered_df['occupation'] == selected_occupation]

if selected_genre != 'All':
    filtered_df = filtered_df[
        filtered_df['genres'].str.contains(selected_genre)
    ]

st.header("Filtered Data Summary")
st.write(f"Total Unique Movies: **{filtered_df['movie_id'].nunique()}**")
st.write(f"Total Ratings: **{len(filtered_df)}**")
    
st.markdown("---")
    
st.header('Genre Breakdown')
st.markdown('The Total Reviews Of Each Genre')
    
genre_counts = filtered_df.assign(genre=filtered_df['genres'].str.split('|')).explode('genre')['genre'].value_counts()
genre_counts_df = genre_counts.reset_index()
genre_counts_df.columns = ['Genre', 'Number of Ratings']
    
fig1 = px.bar(genre_counts_df, 
                x='Genre', 
                y='Number of Ratings', 
                title='Ratings Breakdown by Genre',
                labels={'Genre': 'Genre', 'Number of Ratings': 'Total Ratings'})
st.plotly_chart(fig1)
    
st.markdown("---")
    
st.header('Highest Rated Genres')

genre_ratings_exploded = filtered_df.assign(genre=filtered_df['genres'].str.split('|')).explode('genre')
mean_ratings_by_genre = genre_ratings_exploded.groupby('genre')['rating'].mean().sort_values(ascending=False).reset_index()
mean_ratings_by_genre.columns = ['Genre', 'Mean Rating']

fig2 = px.bar(mean_ratings_by_genre,
                x='Genre',
                y='Mean Rating',
                color='Mean Rating',
                title='Mean Rating by Genre',
                labels={'Genre': 'Genre', 'Mean Rating': 'Average Rating'},
                color_continuous_scale=px.colors.sequential.Viridis)
st.plotly_chart(fig2)
    
st.markdown("---")

st.header('Mean Rating Change Over Time')
st.markdown('The Average Ratings in Reviews Over Time')
    

ratings_with_year = filtered_df.dropna(subset=['year'])
mean_ratings_by_year = ratings_with_year.groupby('year')['rating'].mean().reset_index()
    
fig3 = px.line(mean_ratings_by_year, 
                x='year', 
                y='rating', 
                title='Mean Rating by Movie Release Year',
                labels={'year': 'Movie Release Year', 'rating': 'Average Rating'})
st.plotly_chart(fig3)

st.markdown("---")
    
    
st.header('Best-Rated Movies')
st.markdown('The Best Rated Movies (MIN 5 REVIEWS)')
    
movie_ratings = filtered_df.groupby('title').agg(
    mean_rating=('rating', 'mean'),
    rating_count=('rating', 'count')
).reset_index()
    

top_5_ratings = movie_ratings[movie_ratings['rating_count'] >= 50].sort_values(by='mean_rating', ascending=False).head(5)
    
st.subheader('Top 5 Movies with at least 50 Ratings')
if top_5_ratings.empty:
    st.info("No movies meet this criteria with the current filters.")
else:
    st.dataframe(top_5_ratings)
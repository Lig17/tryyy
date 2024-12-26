import streamlit as st
import plotly.graph_objects as go
from wordcloud import WordCloud
import pandas as pd
from datetime import datetime
from reddit_service import fetch_reddit_data  # Import the Reddit data fetch function
from transformers import pipeline
from PIL import Image
import io

# Initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", framework="pt")

# Function to analyze sentiment
def analyze_sentiment(text):
    try:
        result = sentiment_pipeline(text[:512])  # Limit to 512 characters for better performance
        return result[0]["label"]  # Output: "POSITIVE" or "NEGATIVE"
    except Exception as e:
        return "NEUTRAL"  # Default to neutral if something goes wrong

# Streamlit Layout
st.title("Social Media Monitoring Dashboard")

# Sidebar Filters
st.sidebar.title("Filters")
keyword = st.sidebar.text_input("Search Keyword", "Enter a keyword (e.g., Python)")
limit = st.sidebar.slider("Number of Posts to Fetch", 5, 50, 10)  # Slider for selecting the number of posts

if keyword:
    try:
        # Fetch live Reddit data
        reddit_posts = fetch_reddit_data(keyword, limit=limit)
        df = pd.DataFrame(reddit_posts)

        if not df.empty:
            # Analyze sentiment
            df["sentiment"] = df["title"].apply(analyze_sentiment)

            # Sentiment Distribution Pie Chart
            sentiment_counts = df["sentiment"].value_counts().to_dict()
            sentiment_fig = go.Figure(
                data=[
                    go.Pie(
                        labels=list(sentiment_counts.keys()),
                        values=list(sentiment_counts.values()),
                        hole=0.4,
                        marker=dict(colors=["green", "red", "blue"]),
                    )
                ]
            )
            sentiment_fig.update_layout(title="Sentiment Distribution (Based on Post Titles)")

            # Word Cloud for Post Titles
            wordcloud = WordCloud(
                width=800, height=400, background_color="white"
            ).generate(" ".join(df["title"]))
            wordcloud_image = io.BytesIO()
            Image.fromarray(wordcloud.to_array()).save(wordcloud_image, format="PNG")
            wordcloud_image.seek(0)

            # Subcategories of Negative Sentiments (Dummy Example)
            negative_sub_sentiments = {"Angry": 10, "Sad": 15, "Hateful": 5}
            negative_sub_fig = go.Figure(
                data=[
                    go.Pie(
                        labels=list(negative_sub_sentiments.keys()),
                        values=list(negative_sub_sentiments.values()),
                        hole=0.4,
                        marker=dict(colors=["purple", "orange", "red"]),
                    )
                ]
            )
            negative_sub_fig.update_layout(title="Negative Sentiment Subcategories")

            # Main Dashboard Layout
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Sentiment Distribution")
                st.plotly_chart(sentiment_fig, use_container_width=True)

                st.subheader("Frequent Terms Word Cloud")
                st.image(wordcloud_image, use_column_width=True)

            with col2:
                st.subheader("Negative Sentiment Subcategories")
                st.plotly_chart(negative_sub_fig, use_container_width=True)

            # Messages Section
            st.subheader("Messages")
            for _, row in df.iterrows():
                created_time = datetime.utcfromtimestamp(row["created_utc"]).strftime('%Y-%m-%d %H:%M:%S')
                st.text(f"[{created_time}] {row['author']}: {row['title']}")
        else:
            st.warning(f"No data found for keyword '{keyword}'.")
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")

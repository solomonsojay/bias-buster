import streamlit as st
from transformers import pipeline
from pymongo import MongoClient

# Page config
st.set_page_config(page_title="Bias Buster", page_icon="🧠", layout="centered")

# App title and description
st.title("🧠 Bias Buster")
st.subheader("Understand the sentiment behind the news you read.")
st.markdown("Type a news headline below and click **Analyze** to see if it's Positive, Negative, or Neutral.")

# Text input
headline = st.text_input("📰 News Headline", placeholder="e.g., The economy is booming, but only for the rich.")

# Load sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

# MongoDB connection
uri = "mongodb+srv://solomonsojay:YourStrongPassword123@biasbuster.hdqbfa6.mongodb.net/?retryWrites=true&w=majority&appName=BiasBuster"
client = MongoClient(uri)
db = client["biasdb"]
collection = db["headlines"]

# Analyze and save
if st.button("🔍 Analyze Sentiment"):
    if not headline.strip():
        st.warning("Please enter a headline to analyze.")
    else:
        result = sentiment_pipeline(headline)[0]
        sentiment = result["label"]
        confidence = result["score"]

        # Save to MongoDB
        document = {
            "headline": headline,
            "sentiment": sentiment,
            "confidence": confidence
        }
        collection.insert_one(document)

        # Display results
        st.success(f"✅ Sentiment: **{sentiment}**")
        st.info(f"📊 Confidence Score: **{confidence:.2%}**")
        st.caption("Powered by Hugging Face Transformers • Data stored in MongoDB Atlas")

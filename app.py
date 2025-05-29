import os
import streamlit as st
from dotenv import load_dotenv
from transformers import pipeline
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment
uri = os.environ.get("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(uri)
db = client["biasdb"]
collection = db["headlines"]

# Load sentiment model
sentiment_pipeline = pipeline("sentiment-analysis")

# Streamlit page config
st.set_page_config(page_title="Bias Buster", page_icon="🧠", layout="centered")

# App header
st.title("🧠 Bias Buster")
st.subheader("Understand the sentiment behind the news you read.")
st.markdown("Type a news headline below and click **Analyze** to see if it's Positive, Negative, or Neutral.")

# Headline input
headline = st.text_input("📰 News Headline", placeholder="e.g., The economy is booming, but only for the rich.")

# Analyze button
if st.button("🔍 Analyze Sentiment"):
    if not headline.strip():
        st.warning("Please enter a headline.")
    else:
        # Analyze the headline
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

        # Show results
        st.success(f"✅ Sentiment: **{sentiment}**")
        st.info(f"📊 Confidence: **{confidence:.2%}**")
        st.caption("Analysis by Hugging Face Transformers • Stored in MongoDB Atlas")

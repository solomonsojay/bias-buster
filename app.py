import streamlit as st
from transformers import pipeline
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

st.title("📰 Bias Buster - Sentiment Classifier")

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client["biasbuster"]
collection = db["sentiments"]

sentiment_pipeline = pipeline("sentiment-analysis")

headline = st.text_input("Enter a news headline:")

if st.button("Analyze Sentiment"):
    if headline:
        result = sentiment_pipeline(headline)[0]
        st.write("Sentiment:", result["label"])
        st.write("Confidence:", round(result["score"], 4))

        document = {
            "headline": headline,
            "sentiment": result["label"],
            "confidence": float(result["score"])
        }

        collection.insert_one(document)
        st.success("Result saved to database.")
    else:
        st.warning("Please enter a headline.")

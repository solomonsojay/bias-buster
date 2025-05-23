import streamlit as st
from transformers import pipeline
from pymongo import MongoClient

# AI model
sentiment_pipeline = pipeline("sentiment-analysis")

# MongoDB setup
uri = "mongodb+srv://solomonsojay:YourStrongPassword123@biasbuster.hdqbfa6.mongodb.net/?retryWrites=true&w=majority&appName=BiasBuster"
client = MongoClient(uri)
db = client["biasdb"]
collection = db["headlines"]

# Streamlit UI
st.set_page_config(page_title="Bias Buster", page_icon="🧠")
st.title("🧠 Bias Buster")
st.write("Enter a news headline and detect its sentiment using AI!")

headline = st.text_input("News Headline")

if st.button("Analyze"):
    if not headline.strip():
        st.warning("Please enter a headline.")
    else:
        result = sentiment_pipeline(headline)[0]
        sentiment = result["label"]
        confidence = result["score"]

        # Store result in MongoDB
        document = {
            "headline": headline,
            "sentiment": sentiment,
            "confidence": confidence
        }
        collection.insert_one(document)

        # Display the result
        st.success(f"**Sentiment:** {sentiment}")
        st.info(f"**Confidence:** {confidence:.2%}")

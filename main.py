import streamlit as st
from transformers import pipeline
from pymongo import MongoClient
import warnings
from transformers.utils import logging

# Suppress warnings
logging.set_verbosity_error()
warnings.filterwarnings("ignore")

# Cache the AI model with explicit specification
@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        revision="af0f99b"
    )

# Cache predictions for repeated inputs
@st.cache_data
def analyze_sentiment(text):
    return sentiment_pipeline(text)[0]

# Initialize
sentiment_pipeline = load_model()

# Secure MongoDB connection
uri = st.secrets["MONGODB_URI"]
client = MongoClient(uri)
db = client["biasdb"]
collection = db["headlines"]

# Streamlit UI
st.set_page_config(page_title="Bias Buster", page_icon="🧠", layout="wide")
st.title("🧠 Bias Buster")
st.write("Analyze news headline sentiment with AI!")

# Input and analysis
headline = st.text_input("News Headline", placeholder="Enter a headline to analyze...")

if st.button("Analyze", type="primary"):
    if not headline.strip():
        st.warning("Please enter a headline.")
    else:
        with st.spinner("Analyzing sentiment..."):
            try:
                # Get and display results
                result = analyze_sentiment(headline)
                sentiment = result["label"]
                confidence = result["score"]
                
                # Store in MongoDB
                document = {
                    "headline": headline,
                    "sentiment": sentiment,
                    "confidence": float(confidence)
                }
                collection.insert_one(document)
                
                # Display with colored boxes
                if sentiment == "POSITIVE":
                    st.success(f"✅ **Sentiment:** {sentiment} (Confidence: {confidence:.2%})")
                else:
                    st.error(f"❌ **Sentiment:** {sentiment} (Confidence: {confidence:.2%})")
                    
                st.balloons()  # Celebration effect
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.stop()

# Optional: Show recent analyses
if st.checkbox("Show recent analyses"):
    recent = list(collection.find().sort("_id", -1).limit(5))
    if recent:
        st.write("## Recent Analyses")
        for doc in recent:
            st.write(f"- {doc['headline']}: {doc['sentiment']} ({doc['confidence']:.2%})")
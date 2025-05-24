import streamlit as st

# MUST be first command
st.set_page_config(page_title="Bias Buster", page_icon="🧠", layout="wide")

# Now other imports
from transformers import pipeline
from pymongo import MongoClient
import warnings
from transformers.utils import logging

# Immediately suppress warnings
logging.set_verbosity_error()
warnings.filterwarnings("ignore")

# Initialize MongoDB connection early
@st.cache_resource
def init_db():
    return MongoClient(st.secrets["MONGODB_URI"])

# Cache model loading
@st.cache_resource
def load_model():
    try:
        return pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            revision="af0f99b"
        )
    except Exception as e:
        st.error(f"Model loading failed: {str(e)}")
        st.stop()

# Initialize components
client = init_db()
db = client["biasdb"]
collection = db["headlines"]
sentiment_pipeline = load_model()

# Rest of your UI code below...
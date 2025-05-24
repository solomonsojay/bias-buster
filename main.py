import streamlit as st

# MUST be the first Streamlit command
st.set_page_config(page_title="Bias Buster", page_icon="🧠", layout="wide")

# Now import other libraries AFTER set_page_config
from transformers import pipeline
from pymongo import MongoClient
import warnings
from transformers.utils import logging

# Suppress warnings
logging.set_verbosity_error()
warnings.filterwarnings("ignore")

# Rest of your code remains the same...
@st.cache_resource
def load_model():
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        revision="af0f99b"
    )

# [Keep all other code below exactly as before]
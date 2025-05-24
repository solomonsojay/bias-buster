import streamlit as st
import sys
import subprocess

# MUST be first command
st.set_page_config(page_title="Bias Buster", page_icon="🧠", layout="wide")

def install_packages():
    """Ensure critical packages are installed"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", 
                             "torch==2.3.0+cpu", "--index-url", 
                             "https://download.pytorch.org/whl/cpu"])
    except subprocess.CalledProcessError:
        st.error("Failed to install PyTorch. Please check logs.")
        st.stop()

# Now other imports with try-catch
try:
    from transformers import pipeline
    import torch
    from pymongo import MongoClient
except ImportError:
    install_packages()
    from transformers import pipeline
    import torch
    from pymongo import MongoClient

# Rest of your existing code...
@st.cache_resource
def load_model():
    if not torch.cuda.is_available():
        torch.backends.quantized.engine = 'qnnpack'
    return pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        revision="af0f99b"
    )
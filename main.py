from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os
import traceback

# Load environment variables
load_dotenv()

# Connect to MongoDB
try:
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client["biasbuster"]
    collection = db["articles"]
except Exception as e:
    print("❌ MongoDB Connection Error:", e)
    raise

# Init FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load ML models
try:
    sentiment_model = pipeline("sentiment-analysis")
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception as e:
    print("❌ Model Load Error:", e)
    traceback.print_exc()

# Input format
class ArticleInput(BaseModel):
    headline: str
    content: str

# Analyze endpoint
@app.post("/analyze/")
def analyze(article: ArticleInput):
    try:
        sentiment = sentiment_model(article.headline)[0]
        embedding = embedding_model.encode(article.headline).tolist()

        result = {
            "headline": article.headline,
            "content": article.content,
            "sentiment": sentiment,
            "embedding": embedding
        }

        # Save to MongoDB, but don't return the Mongo insert result
        collection.insert_one(result)

        return {
            "headline": article.headline,
            "sentiment": sentiment["label"],
            "score": sentiment["score"]
        }

    except Exception as e:
        print("❌ Processing Error:", e)
        traceback.print_exc()
        return {"error": "Internal Server Error"}

import os
from transformers import pipeline
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client["biasbuster"]
collection = db["sentiments"]

sentiment_pipeline = pipeline("sentiment-analysis")

headline = "The economy is booming, but only for the rich."
result = sentiment_pipeline(headline)[0]

document = {
    "headline": headline,
    "sentiment": result["label"],
    "confidence": float(result["score"])
}

collection.insert_one(document)
print("Document inserted:", document)

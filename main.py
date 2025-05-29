import os
from dotenv import load_dotenv
from pymongo import MongoClient
from transformers import pipeline

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from environment
uri = os.environ.get("MONGODB_URI")

# Connect to MongoDB
client = MongoClient(uri)
db = client["biasdb"]
collection = db["headlines"]

# Load sentiment model
sentiment = pipeline("sentiment-analysis")

# Analyze a sample headline
text = "The economy is booming, but only for the rich."
result = sentiment(text)[0]

# Save to MongoDB
document = {
    "headline": text,
    "sentiment": result["label"],
    "confidence": result["score"]
}

collection.insert_one(document)
print("Document inserted:", document)

from pymongo import MongoClient
from transformers import pipeline

# Load the AI model
sentiment = pipeline("sentiment-analysis")

# MongoDB URI - update with your password
uri = "mongodb+srv://solomonsojay:YourStrongPassword123@biasbuster.hdqbfa6.mongodb.net/?retryWrites=true&w=majority&appName=BiasBuster"
client = MongoClient(uri)

# Choose DB and collection
db = client["newsdb"]
collection = db["articles"]

# Analyze and insert sample text
text = "The economy is booming, but only for the rich."
result = sentiment(text)[0]

document = {
    "headline": text,
    "sentiment": result["label"],
    "confidence": result["score"]
}

collection.insert_one(document)
print("Document inserted:", document)

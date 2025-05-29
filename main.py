from transformers import pipeline
from pymongo import MongoClient

# Load Hugging Face sentiment analysis pipeline
sentiment = pipeline("sentiment-analysis")

# Connect to MongoDB
uri = "mongodb+srv://solomonsojay:YourStrongPassword123@biasbuster.hdqbfa6.mongodb.net/?retryWrites=true&w=majority&appName=BiasBuster"
client = MongoClient(uri)
db = client["biasdb"]
collection = db["headlines"]

# Headline to test
text = "The economy is booming, but only for the rich."

# Run sentiment analysis
result = sentiment(text)[0]
document = {
    "headline": text,
    "sentiment": result["label"],
    "confidence": result["score"]
}

# Insert into MongoDB
collection.insert_one(document)

# Output to console
print("Document inserted:", document)

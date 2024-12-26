from transformers import pipeline

# Test the sentiment-analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", framework="pt")
result = sentiment_pipeline("I love using Transformers!")
print(result)

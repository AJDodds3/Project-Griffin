from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import torch

# Load FinBERT model and tokenizer (finance-specific tone classification)
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")

def analyze_sentiment(text: str) -> float:
    # Prepare input with explicit truncation and max length for BERT
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits[0].numpy()
    probs = softmax(logits)

    sentiment_score = round(probs[2] - probs[0], 3)  # Bullish - Bearish
    print("Bearish:", round(probs[0], 3))
    print("Neutral:", round(probs[1], 3))
    print("Bullish:", round(probs[2], 3))
    print("Sentiment score:", sentiment_score)

    return sentiment_score

# Run a test case
if __name__ == "__main__":
    text = """
    GameStop stock surged 15% after the company reported strong quarterly earnings 
    and higher-than-expected revenue. Analysts praised the turnaround strategy, 
    calling it a 'new chapter' for the retailer.
    """
    analyze_sentiment(text)
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np

# Load FinBERT model and tokenizer
model_name = 'yiyanghkust/finbert-tone'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

def get_final_sentiment_score(text):
    """
    Returns a well-distributed sentiment score between -1 and 1 using:
    1. The difference between positive and negative probabilities
    2. Damping based on neutral probability
    3. Non-linear scaling for better distribution
    """
    # Tokenize and run through model
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    
    # Get probabilities using softmax
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    probs = probs.detach().numpy()[0]
    
    # Extract probabilities
    neutral_prob = probs[0]
    positive_prob = probs[1]
    negative_prob = probs[2]
    
    # Calculate raw sentiment (difference between positive and negative)
    raw_sentiment = positive_prob - negative_prob
    
    # Apply neutral damping (the more neutral, the closer to zero)
    damped_sentiment = raw_sentiment * (1 - neutral_prob)
    
    # Apply non-linear scaling to prevent clustering at extremes
    final_score = np.sign(damped_sentiment) * (abs(damped_sentiment) ** 0.5)
    
    return float(final_score)

# Test cases
test_texts = [
    "Apple's new product line exceeded all sales expectations, with record-breaking numbers.",
    "The company reported mixed results, meeting some targets but missing others.",
    "Investors are panicking after the disastrous earnings report showed massive losses.",
    "The stock remained unchanged as no significant news was released today.",
    "This revolutionary technology will transform the industry and create huge value.",
    "The earnings were slightly better than expected, though concerns remain about future growth.",
    "Management's guidance disappointed investors, leading to a sharp sell-off.",
    "Analysts are cautiously optimistic about the company's new strategy.",
    "Results were in line with expectations, showing steady but unremarkable growth.",
    "The CEO's comments sparked both enthusiasm and skepticism among analysts."
]

for text in test_texts:
    score = get_final_sentiment_score(text)
    print(f"Text: {text[:80]}...")
    print(f"Final sentiment score: {score:.4f}")
    print("-" * 80)
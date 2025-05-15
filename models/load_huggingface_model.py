from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import os

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
MODEL_DIR = "models/saved_model"

def download_and_save_model():
    """Downloads and saves the Hugging Face model locally."""
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Load and save tokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    tokenizer.save_pretrained(MODEL_DIR)

    # Load and save model
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.save_pretrained(MODEL_DIR)

    print(f"Model downloaded and saved in {MODEL_DIR}")

def load_anomaly_detection_model():
    """Loads the locally saved Hugging Face model for sentiment analysis."""
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)

    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

if __name__ == "__main__":
    download_and_save_model()  # Download and save model before first use

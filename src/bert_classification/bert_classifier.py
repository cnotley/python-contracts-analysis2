import torch
from transformers import BertForSequenceClassification, BertTokenizer
import numpy as np
import logging

class BERTClassifier:
    def __init__(self, model_path, tokenizer='bert-base-uncased', num_labels=3):
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.tokenizer = BertTokenizer.from_pretrained(tokenizer)
            self.model = BertForSequenceClassification.from_pretrained(model_path, num_labels=num_labels)
            self.model.to(self.device)
        except Exception as e:
            logging.error(f"BERT model initialization failed: {e}")
            raise

    def classify(self, text):
        try:
            inputs = self.tokenizer.encode_plus(
                text, add_special_tokens=True, max_length=512, truncation=True,
                padding="max_length", return_attention_mask=True, return_tensors="pt"
            )
            input_ids = inputs["input_ids"].to(self.device)
            attention_mask = inputs["attention_mask"].to(self.device)
            with torch.no_grad():
                outputs = self.model(input_ids, token_type_ids=None, attention_mask=attention_mask)
            logits = outputs.logits
            predicted_category_index = torch.argmax(logits, dim=1).cpu().numpy()[0]
            category_mapping = {0: 'green', 1: 'yellow', 2: 'red'}
            return category_mapping.get(predicted_category_index, "Unknown")
        except Exception as e:
            logging.error(f"Error during classification: {e}")
            return "Error"
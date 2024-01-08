import torch
from transformers import BertForSequenceClassification, BertTokenizer

def save_model(model, save_path):
    """
    Save a trained BERT model.

    Args:
    model (BertForSequenceClassification): The BERT model to save.
    save_path (str): Path where the model should be saved.
    """
    model.save_pretrained(save_path)
    print(f"Model saved to {save_path}")

def load_model(model_path, device):
    """
    Load a trained BERT model.

    Args:
    model_path (str): Path to the saved BERT model.
    device (torch.device): Device to load the model on.

    Returns:
    BertForSequenceClassification: The loaded BERT model.
    """
    model = BertForSequenceClassification.from_pretrained(model_path)
    model.to(device)
    return model

def configure_model(num_labels):
    """
    Configure a new BERT model for sequence classification.

    Args:
    num_labels (int): Number of labels for classification.

    Returns:
    BertForSequenceClassification: The configured BERT model.
    """
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=num_labels)
    return model
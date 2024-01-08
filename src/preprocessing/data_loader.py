import json
import torch
from transformers import BertTokenizer
from torch.utils.data import TensorDataset

def load_json_data(file_path):
    """
    Load data from a JSON file.
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def preprocess_data_for_bert(data, tokenizer, max_length=512):
    """
    Preprocess data for BERT model, including tokenization and generating attention masks.
    """
    input_ids = []
    attention_masks = []
    labels = []

    for entry in data:
        text = entry['text']
        label = entry['label']

        encoded_dict = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=max_length,
            truncation=True,
            padding="max_length",
            return_attention_mask=True,
            return_tensors='pt',
        )
        
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])
        labels.append(label)

    input_ids = torch.cat(input_ids, dim=0)
    attention_masks = torch.cat(attention_masks, dim=0)
    labels = torch.tensor(labels)

    return TensorDataset(input_ids, attention_masks, labels)

def load_and_preprocess_data_for_bert(file_path, bert_model_name='bert-base-uncased'):
    """
    Load and preprocess historical data from a JSON file for BERT.
    """
    data = load_json_data(file_path)
    tokenizer = BertTokenizer.from_pretrained(bert_model_name)
    return preprocess_data_for_bert(data, tokenizer)
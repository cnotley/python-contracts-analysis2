from gpt_keyterm_extractor import GPTKeyTermExtractor
from bert_classifier import BERTClassifier
from bert_trainer import train_model
from config import Config
from data_loader import load_and_preprocess_data_for_bert
from feedback_handler import parse_feedback_data, adjust_terms_based_on_feedback
from historical_data_analysis import HistoricalDataAnalysis
from data_aggregator import DataAggregator
from utility_functions import load_json_data, save_feedback
from feedback_ui import label_terms
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import DataLoader, random_split
import torch

def main():
    # Initialize modules with configurable parameters
    gpt_extractor = GPTKeyTermExtractor(model="text-davinci-003")
    data_aggregator = DataAggregator()
    historical_data_analysis = HistoricalDataAnalysis(Config.HISTORICAL_DATA_PATH)

    if Config.HIGH_MEMORY_MODE:
        # Increase batch sizes and other parameters for high-memory mode
        Config.TRAIN_BATCH_SIZE *= 2
        Config.VALIDATION_BATCH_SIZE *= 2
        
    # Load tokenizer and model for BERT with configurable learning rate
    tokenizer = BertTokenizer.from_pretrained(Config.BERT_TOKENIZER)
    bert_model = BertForSequenceClassification.from_pretrained(Config.BERT_TOKENIZER, num_labels=Config.NUM_LABELS)

    # Load, preprocess, and split data with configurable batch sizes and split ratio
    historical_data_path = Config.HISTORICAL_DATA_PATH
    historical_dataset = load_and_preprocess_data_for_bert(historical_data_path, tokenizer)
    train_size = int(Config.TRAIN_VALIDATION_SPLIT * len(historical_dataset))
    val_size = len(historical_dataset) - train_size
    train_dataset, val_dataset = random_split(historical_dataset, [train_size, val_size])

    train_dataloader = DataLoader(train_dataset, sampler=torch.utils.data.RandomSampler(train_dataset), batch_size=Config.TRAIN_BATCH_SIZE)
    validation_dataloader = DataLoader(val_dataset, sampler=torch.utils.data.SequentialSampler(val_dataset), batch_size=Config.VALIDATION_BATCH_SIZE)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    bert_model.to(device)
    trained_bert_model = train_model(bert_model, train_dataloader, validation_dataloader, device, learning_rate=Config.BERT_LEARNING_RATE)

    # Initialize BERT classifier with the trained model
    bert_classifier = BERTClassifier(trained_bert_model, tokenizer)

    # GPT-4 extraction and BERT classification
    document = "Your document text goes here"
    extracted_terms = gpt_extractor.process_document(document)
    classified_terms = [bert_classifier.classify(term) for term in extracted_terms]

    # Aggregate and format output
    aggregated_data = data_aggregator.aggregate_data(extracted_terms, classified_terms)
    formatted_output = data_aggregator.format_output(aggregated_data)
    print("Aggregated Data:", formatted_output)

    # Feedback processing
    feedback_data = parse_feedback_data(Config.FEEDBACK_DATA_PATH)
    adjusted_terms = adjust_terms_based_on_feedback(extracted_terms, feedback_data)

    # Manual feedback labeling
    # feedback = label_terms(extracted_terms)
    # save_feedback(feedback, "path/to/save/feedback.json")

if __name__ == "__main__":
    main()

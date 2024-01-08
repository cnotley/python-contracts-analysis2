class Config:
    GPT_API_KEY = "your-gpt-4-api-key"
    AZURE_API_VERSION = "2023-09-15-preview"
    AZURE_ENDPOINT = "https://aristotle-canada-east.openai.azure.com/"
    BERT_MODEL_PATH = "path/to/your/fine-tuned-bert-model"
    BERT_TOKENIZER = "bert-base-uncased"
    HISTORICAL_DATA_PATH = "path/to/your/historical/data"
    FEEDBACK_DATA_PATH = "path/to/your/feedback/data"
    MAX_TOKEN_SIZE = 512
    NUM_LABELS = 3
    BERT_LEARNING_RATE = 2e-5
    BERT_MAX_GRAD_NORM = 1.0 
    GPT_CHUNK_SIZE = 4000
    TRAIN_BATCH_SIZE = 16
    VALIDATION_BATCH_SIZE = 16
    TRAIN_VALIDATION_SPLIT = 0.8
    LARGE_DATASET_THRESHOLD = 10000
    HIGH_MEMORY_MODE = False
# Project README

## Overview

This project integrates advanced AI techniques using GPT-4 for key term extraction and BERT for key term classification. It's designed to process text documents, specifically contracts, to extract, classify, and refine key terms. The system improves continuously through a feedback loop and leverages historical data for enhanced performance.

### Features

- GPT-4 based Key Term Extraction
- BERT based Key Term Classification
- Feedback-driven refinement process
- Historical data learning and storage
- Standardization and post-processing for consistency

## Project Structure

project_root/
├── data/
│   ├── training_data.json
│   ├── validation_data.json
│   └── processed_data/
│
├── models/
│   ├── bert_model/
│   └── gpt_model/
│
├── src/
│   ├── preprocessing/
│   │   ├── data_loader.py
│   │   └── feature_engineering.py
│   │
│   ├── gpt_extraction/
│   │   └── gpt_keyterm_extractor.py
│   │
│   ├── bert_classification/
│   │   ├── bert_trainer.py
│   │   ├── bert_classifier.py
│   │   └── model_utils.py
│   │
│   ├── postprocessing/
│   │   └── data_aggregator.py
│   │
│   ├── utils/
│   │   ├── config.py
│   │   ├── utility_functions.py
│   │   ├── feedback_handler.py
│   │   └── historical_data_analysis.py
│   │
│   ├── feedback_loop/
│   │   └── feedback_ui.py
│   │
│   └── main.py
│
├── tests/
│   ├── test_preprocessing.py
│   ├── test_gpt_extraction.py
│   └── test_bert_classification.py
│
└── Dockerfile


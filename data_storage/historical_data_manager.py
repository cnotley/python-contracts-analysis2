import json
import os
import logging

class HistoricalDataManager:
    def __init__(self, storage_dir='historical_data'):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            try:
                os.makedirs(storage_dir)
            except Exception as e:
                logging.error(f"Failed to create storage directory: {e}")
                raise

    def save_data(self, data, file_name):
        path = os.path.join(self.storage_dir, file_name)
        try:
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"Error saving data to {file_name}: {e}")
            raise

    def load_data(self, file_name):
        path = os.path.join(self.storage_dir, file_name)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except Exception as e:
                logging.error(f"Error loading data from {file_name}: {e}")
                raise
        logging.warning(f"File {file_name} not found.")
        return {}
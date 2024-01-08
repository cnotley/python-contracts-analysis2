import json
import os
from collections import Counter
import spacy

class HistoricalDataAnalysis:
    def __init__(self, data_path):
        """
        Initialize the HistoricalDataAnalysis with the path to the historical data.

        Args:
        data_path (str): Path to the historical data file.
        """
        self.data_path = data_path
        self.nlp = spacy.load("en_core_web_sm")

    def load_data(self):
        """
        Load historical data from a file.

        Returns:
        list: List of historical data entries.
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"No historical data found at {self.data_path}")

        with open(self.data_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def analyze_term_frequencies(self, data):
        """
        Analyze the frequency of terms in the historical data.

        Args:
        data (list): List of historical data entries.

        Returns:
        dict: A dictionary with terms as keys and their frequencies as values.
        """
        term_counter = Counter()
        for entry in data:
            if 'term' in entry:
                term_counter[entry['term']] += 1
        return term_counter

    def analyze_term_context(self, data):
        """
        Analyze the context in which terms are used.

        Args:
        data (list): List of historical data entries.

        Returns:
        dict: A dictionary with terms as keys and common contexts as values.
        """
        context_counter = Counter()
        for entry in data:
            if 'term' in entry and 'context' in entry:
                doc = self.nlp(entry['context'])
                for sent in doc.sents:
                    if entry['term'] in sent.text:
                        context_counter[sent.text] += 1
        return context_counter
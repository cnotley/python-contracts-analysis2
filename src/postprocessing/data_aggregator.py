import json
from collections import defaultdict
import spacy

class DataAggregator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def aggregate_data(self, extracted_terms, classified_terms):
        aggregated_data = []
        for term, classification in zip(extracted_terms, classified_terms):
            normalized_term = self.normalize_term(term)
            aggregated_data.append({
                "term": normalized_term,
                "classification": classification
            })
        return aggregated_data

    def format_output(self, aggregated_data):
        return json.dumps(aggregated_data, indent=4)

    def normalize_term(self, term):
        return term.lower().strip()

    def apply_consistency_rules(self, aggregated_data):
        term_mapping = defaultdict(list)
        for item in aggregated_data:
            term_mapping[item['term']].append(item['classification'])

        merged_data = self.merge_similar_terms(term_mapping)
        consistent_data = self.apply_classification_rules(merged_data)
        return consistent_data

    def merge_similar_terms(self, term_mapping):
        """
        Merge similar terms using NLP techniques.

        Args:
            term_mapping (dict): Mapping of terms to their classifications.

        Returns:
            dict: Merged term mapping.
        """
        merged_mapping = defaultdict(list)
        processed_terms = set()

        for term in term_mapping.keys():
            if term not in processed_terms:
                processed_terms.add(term)
                merged_mapping[term].extend(term_mapping[term])
                term_doc = self.nlp(term)

                for other_term in term_mapping.keys():
                    if other_term != term and other_term not in processed_terms:
                        other_term_doc = self.nlp(other_term)
                        if term_doc.similarity(other_term_doc) > 0.8:
                            processed_terms.add(other_term)
                            merged_mapping[term].extend(term_mapping[other_term])

        return merged_mapping

    def apply_classification_rules(self, term_mapping):
        """
        Apply classification rules to the merged term mapping.

        Args:
            term_mapping (dict): Merged term mapping.

        Returns:
            list: List of terms with their most frequent classification.
        """
        consistent_data = []
        for term, classifications in term_mapping.items():
            most_frequent_classification = max(set(classifications), key=classifications.count)
            consistent_data.append({
                "term": term,
                "classification": most_frequent_classification
            })
        return consistent_data
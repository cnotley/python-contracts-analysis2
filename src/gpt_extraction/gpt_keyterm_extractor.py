import openai
from utils import config
from utils.prompt_store import (
    SYSTEM_CONTEXT, construct_prompt_0, construct_prompt_2_append_and_edit
)
from utils.feedback_handler import FeedbackHandler
import logging
import spacy
from collections import Counter

class GPTKeyTermExtractor:
    def __init__(self, model="text-davinci-003"):
        self.model = model
        self.client = openai.AzureOpenAI(
            api_version="2023-09-15-preview",
            api_key=config.Config.GPT_API_KEY,
            azure_endpoint="https://aristotle-canada-east.openai.azure.com/",
        )
        self.feedback_handler = FeedbackHandler()
        self.nlp = spacy.load("en_core_web_sm")
    
    def process_extracted_terms(self, terms):
        """
        Process and merge similar or overlapping terms.

        Args:
            terms (list): List of extracted key terms.

        Returns:
            list: Processed list of unique key terms.
        """
        term_count = Counter(terms)
        unique_terms = set(terms)

        for term in unique_terms:
            doc1 = self.nlp(term)
            for other_term in unique_terms:
                if term != other_term:
                    doc2 = self.nlp(other_term)
                    similarity = doc1.similarity(doc2)
                    if similarity > 0.8:
                        term_count[term] += term_count[other_term]
                        term_count[other_term] = 0

        processed_terms = [term for term, count in term_count.items() if count > 0]
        return processed_terms

    def chunk_document(self, document, max_chunk_size=4000):
        words = document.split(' ')
        chunks = []
        current_chunk = ''
        for word in words:
            if len(current_chunk) + len(word) + 1 > max_chunk_size:
                chunks.append(current_chunk)
                current_chunk = word
            else:
                current_chunk += ' ' + word
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

    def extract_key_terms_initial(self, chunk):
        prompt = SYSTEM_CONTEXT + "\n\n" + construct_prompt_0(chunk)
        response = self.client.Completion.create(
            engine=self.model, prompt=prompt, max_tokens=150
        )
        return response.choices[0].text.strip()

    def extract_key_terms_iterative(self, chunk, key_terms_so_far):
        adjusted_prompt = self.feedback_handler.adjust_prompt(construct_prompt_2_append_and_edit(chunk, key_terms_so_far))
        response = self.client.Completion.create(
            engine=self.model, prompt=adjusted_prompt, max_tokens=150
        )
        return response.choices[0]._text.strip()

    def process_document(self, document, feedback_data=None):
        if feedback_data:
            self.feedback_handler.update_feedback(feedback_data)
        try:
            chunks = self.chunk_document(document)
            all_key_terms = []
            for chunk in chunks:
                extracted_terms_initial = self.extract_key_terms_initial(chunk)
                extracted_terms_iterative = self.extract_key_terms_iterative(chunk, extracted_terms_initial)
                combined_terms = extracted_terms_initial + extracted_terms_iterative
                processed_terms = self.process_extracted_terms(combined_terms)
                all_key_terms.extend(processed_terms)
            return all_key_terms
        except Exception as e:
            logging.error(f"Error processing document: {e}")
            return []
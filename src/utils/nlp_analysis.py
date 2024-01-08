import spacy
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd

nltk.download('stopwords')

class NLPAnalysis:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.summarizer = pipeline("summarization")
        self.stop_words = stopwords.words('english')
        self.vectorizer = TfidfVectorizer(stop_words=self.stop_words)

    def named_entity_recognition(self, text):
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

    def summarize_text(self, text):
        try:
            summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)
            return summary[0]['summary_text']
        except Exception as e:
            print(f"Summarization error: {e}")
            return text

    def semantic_similarity(self, term1, term2):
        doc1 = self.nlp(term1)
        doc2 = self.nlp(term2)
        return doc1.similarity(doc2)

    def tfidf_analysis(self, documents):
        vectors = self.vectorizer.fit_transform(documents)
        feature_names = self.vectorizer.get_feature_names_out()
        dense = vectors.todense()
        return pd.DataFrame(dense, columns=feature_names)
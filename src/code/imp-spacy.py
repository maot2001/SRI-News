import ir_datasets
import spacy
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.matutils import corpus2dense
import numpy as np

nlp = spacy.load("en_core_web_sm")

dataset = ir_datasets.load("cranfield")

documents = [doc.text for doc in dataset.docs_iter()]

def tokenization_spacy(texts):
  tokenized_texts = []
  for text in texts:
    doc = nlp(text)
    tokens = [(token.text, token.lemma_, token.pos_) for token in doc if not token.is_space and not token.is_punct and \
               not token.is_stop and not token.is_digit]
    tokenized_texts.append(tokens)
  return tokenized_texts

tokenized_docs = tokenization_spacy(documents[:10])
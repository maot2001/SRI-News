import ir_datasets
import spacy
from gensim.corpora import Dictionary
from gensim.models import TfidfModel

dictionary = {}

def tokenization_spacy(texts):
  return [[token.text for token in nlp(doc) if token.is_alpha and not token.is_stop] 
          for doc in texts]

def filter_tokens_by_occurrence(tokenized_docs, no_below=2, no_above=0.5):
  global dictionary
  dictionary = Dictionary(tokenized_docs)
  dictionary.filter_extremes(no_below=no_below, no_above=no_above)

  filtered_words = [word for _, word in dictionary.iteritems()]
  filtered_tokens = [
      [word for word in doc if word in filtered_words]
      for doc in tokenized_docs
  ]

  return filtered_tokens

def build_vocabulary(dictionary):
  return list(dictionary.token2id.keys())

def vector_representation(tokenized_docs, dictionary):
  model_tfidf = TfidfModel(dictionary=dictionary, normalize=True)
  return [model_tfidf[dictionary.doc2bow(tokens)] for tokens in tokenized_docs]

nlp = spacy.load("en_core_web_sm")
dataset = ir_datasets.load("cranfield")
documents = [doc.text for doc in dataset.docs_iter()]

tokenized_docs = filter_tokens_by_occurrence(tokenization_spacy(documents[:10]))
vocabulary = build_vocabulary(dictionary)
vector_repr = vector_representation(tokenized_docs, dictionary)

import gensim
import spacy
from sympy import sympify, to_dnf, Not, And, Or
import nltk
import ir_datasets

nlp = spacy.load("en_core_web_sm")


dataset = ir_datasets.load("cranfield")
documents = [doc.text for doc in dataset.docs_iter()]

def tokenization_spacy(texts):
  return [[token for token in nlp(doc) if token.is_alpha and not token.is_stop] 
          for doc in texts]

def remove_stopwords_spacy(tokenized_docs):
  stopwords = spacy.lang.en.stop_words.STOP_WORDS
  return [
      [token for token in doc if token.text not in stopwords] for doc in tokenized_docs
  ]


def remove_noise_spacy(tokenized_docs):
  return [[token for token in doc if token.is_alpha] for doc in tokenized_docs]

def morphological_reduction_spacy(tokenized_docs, use_lemmatization=True):
  stemmer = nltk.stem.PorterStemmer()
  return [
    [token.lemma_ if use_lemmatization else stemmer.stem(token.text) for token in doc]
    for doc in tokenized_docs
  ]

def convert_to_text(tokenized_docs):
  return[
    [token.text for token in doc] for doc in tokenized_docs
  ]

def query_to_dnf(query):
    processed_query = ""
    q = query.split(" ")
    for i in q:
        if i == "AND":
            processed_query=processed_query + " & "
        elif i == "OR":
            processed_query =processed_query + " | "
        elif i=="NOT":
            processed_query =processed_query + " ~ "
        else:
            processed_query = processed_query + " " + i
    
    query_expr = sympify(processed_query, evaluate=False)
    query_dnf = to_dnf(query_expr, simplify=True)

    return query_dnf

tokenized_docs = morphological_reduction_spacy(remove_stopwords_spacy(remove_noise_spacy(tokenization_spacy(documents))), True)


dictionary = gensim.corpora.Dictionary(tokenized_docs)
vocabulary = list(dictionary.token2id.keys())
corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

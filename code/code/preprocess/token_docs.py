from gensim.corpora import Dictionary
from gensim.models import TfidfModel
import spacy
nlp = spacy.load("en_core_web_sm")
#from . 
import elements

def tokenization_spacy(texts):
    """Give de lemmatization of all the words in the texts

    Args:
        texts (list(str)): the texts you want to process 

    Returns:
        (list(list(str))): for each token in each text, return its lemma
    """
    return [[token.lemma_.lower() for token in nlp(doc) if token.is_alpha and not token.is_stop] 
            for doc in texts]

def filter_tokens_by_occurrence(tokenized_docs, no_below=0, no_above=1.0):
    """Filters the words by occurrence and creates the word dictionary

    Args:
        tokenized_docs (list(list(str))): the tokens you want to process
        no_below (int): Keep tokens which are contained in at least `no_below` documents.
        no_above (float): Keep tokens which are contained in no more than `no_above` documents
                            (fraction of total corpus size, not an absolute number).

    Returns:
        (gensim.corpora.Dictionary, list(list(str))): the dictionary of all words and tokens filtered by occurrence
    """
    dictionary = Dictionary(tokenized_docs)
    dictionary.filter_extremes(no_below=no_below, no_above=no_above)

    filtered_words = [word for _, word in dictionary.iteritems()]
    filtered_tokens = [
        [word for word in doc if word in filtered_words]
        for doc in tokenized_docs
    ]

    return dictionary, filtered_tokens

def build_vocabulary(dictionary):
    return list(dictionary.token2id.keys())
  
def vector_representation(tokenized_docs, dictionary, vocabulary=None, idfs=None):
    """Using gensim.models.TfidfModel and the data body generates the tf-idf for each word in a document.
    """
    model_tfidf = TfidfModel(dictionary=dictionary)
    words = []

    if vocabulary:
        for i in range(len(dictionary.token2id)):
            print(dictionary.id2token[i])
            print(model_tfidf.idfs.get(i))
            words.append(elements.Words(dictionary.id2token[i], model_tfidf.idfs.get(i)))

    if idfs:
        for i in range(len(idfs)):
            model_tfidf.idfs[i] = idfs[i]

    return [model_tfidf[dictionary.doc2bow(tokens)] for tokens in tokenized_docs], words
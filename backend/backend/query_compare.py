from .preprocess import token_docs as tok
from . import utils
import numpy as np
import threading

def search(query_vector, found_words, min, max, result):
    """Using cosine similarity, determine the distance of the query to the document, if the document is in the range (min, max)
    """
    matrix = np.zeros((max-min, len(found_words)))
    docs = [False] * (max-min)

    for i in range(len(found_words)):
        for doc in found_words[i]['docs']:
            if doc['id'] < min: continue
            if doc['id'] >= max: break
            matrix[doc['id'] - min][i] = doc['tf-idf']
            docs[doc['id'] - min] = True

    for i in range(len(docs)):
        if docs[i]:
            doc_vector = [val for val in matrix[i]]
            compare = utils.sum_mult_vector(query_vector, doc_vector)/ (utils.sum_dist_vector(query_vector) * utils.sum_dist_vector(doc_vector))
            result.append((i + min, compare))

def recive_query_tf_idf(query, data_words):
    """Finds the query words in the corpus and separates the work into threads to optimize performance
    """
    dictionary, tokenized_docs = tok.filter_tokens_by_occurrence(tok.tokenization_spacy([query]))
    vocabulary = tok.build_vocabulary(dictionary)
    idfs, result, found_words = [], [], []

    for word in vocabulary:
        aux = utils.binary_search(word, data_words)
        if aux == -1: aux = tok.elements.Words(word, 0)
        idfs.append(aux['idf'])
        found_words.append(aux)

    query_vector, _ = tok.vector_representation(tokenized_docs, dictionary, idfs=idfs)
    query_vector = [val[1] for val in query_vector[0]]

    hilo1 = threading.Thread(target=search, args=(query_vector, found_words, 0, 2000, result))
    hilo1.start()

    hilo2 = threading.Thread(target=search, args=(query_vector, found_words, 2000, 4000, result))
    hilo2.start()

    hilo3 = threading.Thread(target=search, args=(query_vector, found_words, 4000, 6000, result))
    hilo3.start()

    hilo4 = threading.Thread(target=search, args=(query_vector, found_words, 6000, 8000, result))
    hilo4.start()

    hilo5 = threading.Thread(target=search, args=(query_vector, found_words, 8000, 10000, result))
    hilo5.start()

    hilo1.join()
    hilo2.join()
    hilo3.join()
    hilo4.join()
    hilo5.join()

    return result
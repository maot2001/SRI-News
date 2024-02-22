import json
import os
from . import query_compare
from . import summarizer
from .preprocess import elements

def charge_bd():
    route = os.path.join(os.getcwd(), "backend\\data", "words.json")

    with open(route, 'r', encoding='utf-8') as file:
        data_words = json.load(file)

    route = os.path.join(os.getcwd(), "backend\\data", "docs.json")

    with open(route, 'r', encoding='utf-8') as file:
        data_docs = json.load(file)

    return data_words, data_docs

def run(query, data_words, data_docs):
    """Receives the query and loads the database to use it (those functionalities must be separated)
    """
    result = []
    try: query = elements.Docs(query)
    except: 
        print("error")
        return None
                                            
    compare = query_compare.recive_query_tf_idf(query.text, data_words)
    compare = sorted(compare, key=lambda x: x[1], reverse=True)

    for index in compare[:10]:
        doc = data_docs[index[0]]
        reduct = summarizer.summarize(doc['text'])
        result.append((doc['title'], reduct, doc['authors']))
        #result.append(elements.Docs(doc['url'], doc['title'], reduct, doc['authors']))

    return result
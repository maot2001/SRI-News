import json
import os
import query_compare
import summarizer
from preprocess import elements

def run(query):
    """Receives the query and loads the database to use it (those functionalities must be separated)
    """
    result = []
    try: result.append(elements.Docs(query))
    except: return None

    route = os.path.join(os.getcwd(), "code\\preprocess", "words.json")

    with open(route) as file:
        data_words = json.load(file)

    route = os.path.join(os.getcwd(), "code\\preprocess", "docs.json")

    with open(route) as file:
        data_docs = json.load(file)
                                                #cambiar query a doc.text
    compare = query_compare.recive_query_tf_idf(query, data_words)
    compare = sorted(compare, key=lambda x: x[1], reverse=True)

    for index in compare[:10]:
        doc = data_docs[index[0]]
        reduct = summarizer.summarize(doc['text'])
        result.append(elements.Docs(doc['url'], doc['title'], reduct, doc['authors']))

    return result
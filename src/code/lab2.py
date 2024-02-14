import gensim
import spacy
from sympy import sympify,simplify,  to_dnf, Not, And, Or, logic
import nltk
import ir_datasets


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

def query_to_dnf(query):
    processed_query = ""
    try:
        q = query.split(" ")
    except ex:
        q = [query]
    #Se recorre cada elemento de la query y se parsea a un simbolo reconocido
    for i in q:
        if i == "AND":
            processed_query=processed_query + " & "
        elif i == "OR":
            processed_query =processed_query + " | "
        elif i=="NOT":
            processed_query =processed_query + " ~ "
        else:
            processed_query = processed_query + " " + i
    #Se lleva la query a una expresion sympify para poder trabajar con ella
    query_expr = sympify(processed_query, evaluate=False)
    #Se lleva a forma normal disyunitiva
    query_dnf = to_dnf(query_expr, simplify=True)

    return query_dnf

def get_clean_query(query):
    q = query_to_dnf(query)
    # hace una especie de interseccion de la query para no repetir
    # en la documentacion los desarrolladores no saben bien que hace esto(y son seniors), 
    # solo que hace las expresiones mas simples
    clean_q = simplify(q)
    # .args me devuelve una tupla con los implicados en el or(si es un or, como debe ser) 
    tup = clean_q.args
    res = [] 
    # deberia quedar cada forma conjuntiva en una tupla
    if not type(clean_q) == Or:
        res.append(tup)
        return res
    for s in tup:
        if type(s)==And:
            res.append(s.args)
        else: 
            res.append(s)
    return res

def get_matching_docs(query_dnf):
    """Por cada documento analizo las queries y si se cumple los agrego a una lista

    Args:
        query_dnf (): _Es una lista con distintos tipos, pueden ser símbolos de sympy o tuplas de símbolos de sympy_

    Returns:
        _List<List<String>>_: _La lista de todos los documentos d_i tales que sim(d_i, query_dnf)=1_
    """
    global tokenized_docs, dictionary, corpus
    matching_documents = []
    for doc in tokenized_docs:
        for i in query_dnf:
            query_successfully = False
            if type(i) == tuple:
                success = True
                for j in i:
                    is_not = False
                    if type(j) == Not:
                        is_not = True
                        w = str(j.args[0])
                    else: w = str(j)
                    contains = w in doc
                    if is_not and not contains:
                        success = success and not contains
                    elif not is_not and contains:
                        success = success and contains
                    else: 
                        success = success and False
                        break
                if success:
                    query_successfully = True
                    matching_documents.append(doc)
                    break
            else:
                is_not = False
                if type(i) == Not:
                    is_not = True
                    w = str(i.args[0])
                else: w = str(i)
                contains = w in doc
                if is_not and not contains:
                    query_successfully = True
                    matching_documents.append(doc)
                    break
                elif not is_not and contains:
                    query_successfully = True
                    matching_documents.append(doc)
                    break
            if query_successfully:
                break
    return matching_documents



nlp = spacy.load("en_core_web_sm")
dataset = ir_datasets.load("cranfield")
documents = [doc.text for doc in dataset.docs_iter()]
tokenized_docs = morphological_reduction_spacy(remove_stopwords_spacy(remove_noise_spacy(tokenization_spacy(documents))), True)
dictionary = gensim.corpora.Dictionary(tokenized_docs)
vocabulary = list(dictionary.token2id.keys())
corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

#Test
query = "( flow AND wing AND randomPalabraQueNoEsta ) "
print(query_to_dnf(query))
query = get_clean_query(query)
print(query)
x = get_matching_docs(query)
print(len(x))


dictionary = gensim.corpora.Dictionary(tokenized_docs)
vocabulary = list(dictionary.token2id.keys())
corpus = [dictionary.doc2bow(doc) for doc in tokenized_docs]

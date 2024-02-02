import ir_datasets
import spacy
from gensim.corpora import Dictionary
from gensim.models import TfidfModel

# Variable para guardar un Dictionary de gensim, tiene par de funcionalidades utiles como filtros, conversiones a Bag of Word, iteradores
dictionary = {}

# Filtro de documentos
def tokenization_spacy(texts):
  # Retorna una lista de listas, cada lista contiene el texto de los token que son palabras, pero no stopwords (nexos gramaticales)
  return [[token.text for token in nlp(doc) if token.is_alpha and not token.is_stop] 
          for doc in texts]

# Filtro de ocurrencia
def filter_tokens_by_occurrence(tokenized_docs, no_below=2, no_above=0.5):
  global dictionary
  dictionary = Dictionary(tokenized_docs)
  # El filtro de extremos mantiene los documentos que aparecen al menos no_below veces y no mas de no_above veces (no_above es una fraccion del corpus de datos)
  dictionary.filter_extremes(no_below=no_below, no_above=no_above)

  filtered_words = [word for _, word in dictionary.iteritems()]
  # Se eliminan las palabras fuera del diccionario
  filtered_tokens = [
      [word for word in doc if word in filtered_words]
      for doc in tokenized_docs
  ]

  return filtered_tokens

# Se construye un vocabulario (diccionario sin ocurrencia)
def build_vocabulary(dictionary):
  return list(dictionary.token2id.keys())

# Se determina el TF-IDF de cada token en cada documento
def vector_representation(tokenized_docs, dictionary):
  # Retorna una lista de listas, cada lista contiene una tupla (numero de la palabra en vocabulary, valor de TF-IDF para cada documento)
  model_tfidf = TfidfModel(dictionary=dictionary, normalize=True)
  return [model_tfidf[dictionary.doc2bow(tokens)] for tokens in tokenized_docs]

# Carga de datos
nlp = spacy.load("en_core_web_sm")
dataset = ir_datasets.load("cranfield")
documents = [doc.text for doc in dataset.docs_iter()]

# Pre-procesamiento de documentos (Separacion de tokens y filtro de ocurrencia)
tokenized_docs = filter_tokens_by_occurrence(tokenization_spacy(documents[:10]))

# La construccion del vocabulario es importante porque queda en cada posicion las palabras de los documentos, lo cual se pierde en vector_repr
# Si hacen print(vocabulary) y print(vector_repr) entenderan
vocabulary = build_vocabulary(dictionary)

# Aqui se guarda la relacion explicada en vector_representation
vector_repr = vector_representation(tokenized_docs, dictionary)

# Ver relacion de la palabra 1 en los documentos 0 y 1, donde el valor de TF-IDF asociado es diferente para cada documento
print(vocabulary)
print()
for i in range(len(vector_repr)):
  print(f'doc {i}: {vector_repr[i]}')
  print()

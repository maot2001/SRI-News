import json
from operator import attrgetter
#from . 
import token_docs

# Carga de datos
with open('backend//data//docs.json', 'r', encoding='utf-8') as file:
    data_docs = json.load(file)

texts = []
for doc in data_docs:
    texts.append(doc['text'])

# Pre-procesamiento de documentos (Separacion de tokens y filtro de ocurrencia)
dictionary, tokenized_docs = token_docs.filter_tokens_by_occurrence(token_docs.tokenization_spacy(texts[:10000]))

# La construccion del vocabulario es importante porque queda en cada posicion las palabras de los documentos, lo cual se pierde en vector_repr
# Si hacen print(vocabulary) y print(vector_repr) entenderan
vocabulary = token_docs.build_vocabulary(dictionary)

# Aqui se guarda la relacion explicada en vector_representation
vector_repr, words = token_docs.vector_representation(tokenized_docs, dictionary, vocabulary=vocabulary)

for i in range(len(vector_repr)):
    for j in vector_repr[i]:
        words[j[0]].docs.append((i, j[1]))

words = sorted(words, key=attrgetter('word'))

words_json = json.dumps([word.to_dict() for word in words], indent=4, ensure_ascii=False)
with open('backend//data//words.json', 'w', encoding='utf-8') as file:
    file.write(words_json)
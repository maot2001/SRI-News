import json
import threading
import time
import elements

def to_docs(data, min, max):
    """Create docs with the specified data in range(min, max)
    """
    count = min
    for i in range(min, max):
        try:
            url = data[i]['link']
            if url: 
                docs.append(elements.Docs(url))
                results.append(count)
            else: results.append(f'url in {count}')
        except:
            results.append(f'error in {count}')
        count += 1

docs = []
results = []

with open('data.json') as file:
    data = json.load(file)

hilo1 = threading.Thread(target=to_docs, args=(data, 4000, 6200))
hilo1.start()

hilo2 = threading.Thread(target=to_docs, args=(data, 6200, 8400))
hilo2.start()

hilo3 = threading.Thread(target=to_docs, args=(data, 8400, 10600))
hilo3.start()

hilo4 = threading.Thread(target=to_docs, args=(data, 10600, 12800))
hilo4.start()

hilo5 = threading.Thread(target=to_docs, args=(data, 12800, 15000))
hilo5.start()

hilo1.join()
hilo2.join()
hilo3.join()
hilo4.join()
hilo5.join()

docs_json = json.dumps([doc.to_dict() for doc in docs], indent=4, ensure_ascii=False)
with open('docs.json', 'w', encoding='utf-8') as archivo_json:
    archivo_json.write(docs_json)

print(results)
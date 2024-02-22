from django.shortcuts import render
import json
from django.http import HttpResponse, JsonResponse
from . import run

busqueda=''
data_words=[]
data_docs=[]

def index(request):
    return render(request, 'index.html', {})


def news_find(request):
    global data_words, data_docs
    contexto = {
        'mensaje':'Notifind'
    }
    data_words, data_docs = run.charge_bd()
    return render(request, 'news_find.html',contexto)

def buscar(request):
    global busqueda, data_words, data_docs
    if request.method == 'POST':
        datos_json=json.loads(request.body.decode('utf-8'))
        busqueda=datos_json.get('busqueda','')
        resultados_varios=run.run(busqueda, data_words, data_docs)
        return JsonResponse({'resultado': resultados_varios})
    return JsonResponse({'status': 'error'})

def resultado(request):
    global busqueda
    resultado = busqueda
    return JsonResponse({'resultado': resultado})
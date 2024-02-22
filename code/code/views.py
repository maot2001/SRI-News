from django.http import HttpResponse
from . import run

def work(request):
    result = run.run(request)
    if result: return HttpResponse(result)
    return HttpResponse("URL error")
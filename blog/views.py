from django.shortcuts import render

# Inclui a classe HttpResponse
from django.http import HttpResponse

# Define uma function view chamada index
def index(request):
    # return HttpResponse('Olá Django - index')
    return render(request, 'index.html', {'titulo': 'Últimos Artigos'})


# Define uma function view chamada ola.
def ola(request):
    # return HttpResponse('Olá Django')
    # return render(request, 'index.html')
    return render(request, 'home.html')

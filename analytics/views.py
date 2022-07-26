import base64
import io
from django.shortcuts import render
from django.http import HttpResponse
import urllib

from .utils import programas,ricardoDefesas

def index(request):
    dados = programas.load()
    return render(request, 'analytics/index.html', {'dados': dados })

def ricardo_defesas(request):
    dados = ricardoDefesas.loadNivel()
    defesas_curso = ricardoDefesas.loadDefesasCurso()
    return render(request, 'analytics/ricardo_defesas.html', {'df': dados['df'], 'nivel_plot': dados['nivel_plot'], 'defesas_curso' : defesas_curso })

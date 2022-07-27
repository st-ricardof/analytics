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
    defesas_programa_curso = ricardoDefesas.loadDefesasProgramaCurso()
    return render(request, 'analytics/ricardo_defesas.html', {'df': dados['df'], 'nivel_plot': dados['nivel_plot'], 'defesasPorCurso' : defesas_programa_curso['defesasPorCurso'], 'defesasPorPrograma': defesas_programa_curso['defesasPorPrograma'] })

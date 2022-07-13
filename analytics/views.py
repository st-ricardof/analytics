import base64
import io
from django.shortcuts import render
from django.http import HttpResponse
import urllib

from .utils import programas

def index(request):
    dados = programas.load()
    return render(request, 'analytics/index.html', {'dados': dados })
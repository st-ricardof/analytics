from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ricardo/defesas', views.ricardo_defesas, name='ricardo_defesas'),
]

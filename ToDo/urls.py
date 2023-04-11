from ToDo.views import *
from django.urls import path

app_name = 'ToDo'

urlpatterns = [
    path('', index, name='index')
]

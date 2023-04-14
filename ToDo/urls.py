from ToDo.views import *
from django.urls import path

app_name = 'ToDo'

urlpatterns = [
    path('', index, name='index'),
    path('post_json/', post_data, name="post_data"),
    path('show_json/', show_json, name="show_json"),
    path('delete_data/', delete_data, name="delete_data"),
    path('edit_data/', edit_data, name="edit_data"),
    path('edit_finished/', finished_data, name="finished_data"),
]

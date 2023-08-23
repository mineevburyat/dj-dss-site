from . import views
from django.urls import path

app_name = 'search'
urlpatterns = [
    path('', views.result, name='result_list'),
    
]
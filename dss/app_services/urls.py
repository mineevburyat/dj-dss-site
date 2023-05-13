from django.contrib import admin
from django.urls import path
from .views import IndexView, ServiceViewByCategory, DetailService, ListService

app_name = 'app_services'

urlpatterns = [
    path('', ListService.as_view(), name='all'),
    path('<str:category>/', ServiceViewByCategory.as_view(), name='categoryservice'),
    path('detail/<str:slug>', DetailService.as_view(), name='detail'),
]
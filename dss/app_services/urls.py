from django.contrib import admin
from django.urls import path
from .views import IndexView, ServiceViewByCategory

app_name = 'app_services'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('str:<category>/', ServiceViewByCategory.as_view(), name='categoryservice'),
]
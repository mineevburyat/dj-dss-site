from django.contrib import admin
from django.urls import path
from .views import IndexView

app_name = 'app_services'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('str:<category>/', )
]
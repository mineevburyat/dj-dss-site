from django.contrib import admin
from django.urls import path
from .views import DetailServiceView, ListServiceView

app_name = 'app_services'

urlpatterns = [
    path('', ListServiceView.as_view(), name='all'),
    path('<str:category>/', ListServiceView.as_view(), name='categoryservice'),
    path('detail/<str:slug>', DetailServiceView.as_view(), name='detail'),
]
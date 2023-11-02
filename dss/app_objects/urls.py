from django.contrib import admin
from django.urls import path
from .views import IndexView, DetailObjectView, ListObjectsView, DetailAreaView

app_name = 'app_objects'

urlpatterns = [
    path('', ListObjectsView.as_view(), name='index'),
    path('<str:slug>', DetailObjectView.as_view(), name='detail'),
    path('<str:obj_slug>/<str:slug>/', DetailAreaView.as_view(), name='area')
]
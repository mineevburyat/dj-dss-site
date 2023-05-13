from django.urls import path

from .views import Home

urlpatterns = [
    # path('', views.home, name='index'),
    path('', Home.as_view(), name='index')
]
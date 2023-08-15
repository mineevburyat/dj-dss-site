from django.contrib import admin
from django.urls import path
from .views import DetailServiceView, ListServiceView, ListTypeServiceView, campingview, sectionview

app_name = 'app_services'

urlpatterns = [
    # path('', ListServiceView.as_view(), name='all'),
    path('camping/', campingview, name='camping'),
    path('hardsection/<slug:section>/', sectionview, name='hardsection'),
    path('<slug:category>/', ListTypeServiceView.as_view(), name='categoryservice'),
    path('<slug:category>/<slug:typesrvc>', ListServiceView.as_view(), name='listservice'),
    path('detail/<slug:slug>/', DetailServiceView.as_view(), name='detail'),
    
    
]
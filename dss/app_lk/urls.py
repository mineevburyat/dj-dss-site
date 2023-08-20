from django.urls import path
from .views import lk_view, shedule_view

app_name = 'app_lk'
urlpatterns = [
    path('', lk_view, name='lk'),
    path('shedule', shedule_view, name='shedule_1c')
]
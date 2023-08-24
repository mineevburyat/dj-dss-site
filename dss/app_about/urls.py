from django.contrib import admin
from django.urls import path
from .views import (IndexView,
                    ManagmentView,
                    DTurView,
                    DocumentsView,
                    ContactsView,
                    VacantView,
                    ZakupsView,
                    ReseptionView)

app_name = 'app_objects'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('managments/', ManagmentView.as_view(), name="managment"),
    path('3dtur/', DTurView.as_view(), name="3dtur"),
    path('documents/', DocumentsView.as_view(), name="documents"),
    path('contacts/', ContactsView.as_view(), name="contacts"),
    path('job/', VacantView.as_view(), name="job"),
    path('purchases/', ZakupsView.as_view(), name="purchases"),
    path('reseption/', ReseptionView.as_view(), name="reseption"),
]
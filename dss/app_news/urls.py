
from django.urls import path
from .views import (ImageGalleryView,
                    ImageDetailView, 
                    ImageEditForm,
                    ImageDeleteForm
)


app_name = 'app_news'
urlpatterns = [
    path('', ImageGalleryView.as_view(), name='list'),
    path('<slug:slug>/', ImageDetailView.as_view(), name='detailimg'),
    path('<slug:slug>/edit/', ImageEditForm.as_view(), name='img_edit'),
    path('<slug:slug>/del/', ImageDeleteForm.as_view(), name='img_del')
]

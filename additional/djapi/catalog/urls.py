from django.urls import path, re_path
from . import views


urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'books/', views.BookListView.as_view(), name='books'),
    re_path(r'^books/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    # re_path(r'^book/(?P<pk>\d+)$', views.book_detail_view, name='book-detail'),
]
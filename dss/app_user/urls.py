from django.contrib import admin
from django.urls import path
from .views import AuthView, MyLogoutView, RegisterUserView, ProfileEditView, VerificationView



app_name = 'user'

urlpatterns = [
    # path('logout', products, name='index'),
    path('login', AuthView.as_view(), name='login'),
    path('register', RegisterUserView.as_view(), name='register'),
    path('profile/<int:pk>', ProfileEditView.as_view(), name='profile'),
    path('logout', MyLogoutView.as_view(), name='logout'),
    path('verificated/<str:email>/<uuid:code>', VerificationView.as_view(), name='verificated'),
]

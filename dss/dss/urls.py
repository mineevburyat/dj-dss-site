"""
URL configuration for dss project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('home.urls', namespace='home')),
    path('lk/', include('app_lk.urls', namespace='lk')),
    path('objects/', include('app_objects.urls', namespace='objects')),
    path('services/', include('app_services.urls', namespace='services')),
    path('about/', include('app_about.urls', namespace='about')),
    path('user/', include('app_user.urls', namespace='user')),
    path('mediafiles/', include('app_mediafiles.urls', namespace='app_mediafiles')),
    path('news/', include('app_news.urls', namespace='news')),
    path('search', include('app_search.urls', namespace='search')),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
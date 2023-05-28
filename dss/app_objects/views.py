from django.views.generic.base import TemplateView
from common.mixins import TitleMixin, ObjectsMixin
from .models import Object, ObjectGallery
from django.views.generic.detail import DetailView
from django.views.generic import ListView


class IndexView(TitleMixin, TemplateView):
    template_name = 'app_objects/index.html'
    title = "ДСС:объекты"
    

class DetailObjectView(TitleMixin, ObjectsMixin, DetailView):
    model = Object
    context_object_name = 'object'
    template_name = 'app_objects/detail.html'
    title = "ДСС: подробнее"
    objects = Object.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = ObjectGallery.objects.filter(obj=self.request.)
        return context

class ListObjectsView(TitleMixin, ListView):
    model = Object
    context_object_name = 'objects'
    template_name = 'app_objects/index.html'
    title = "ДСС: список объектов"
    
    # def get_queryset(self):
    #     category = self.kwargs.get('category')
    #     if category:
    #         services = Service.objects.filter(category=category)
    #     else:
    #         services = Service.objects.all()
    #     return services

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['category'] = self.kwargs.get('category')
    #     return context
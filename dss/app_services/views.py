from django.shortcuts import get_object_or_404
from django.db import models
from .models import Service, TypeService, CHOICE_CATEGORY
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from common.mixins import TitleMixin
from django.http import Http404
from django.db.models import Q
# from common.mixins import TitleMixin
from app_news.models import News


class DetailServiceView(TitleMixin, DetailView):
    model = Service
    context_object_name = 'service'
    template_name = 'app_services/detail.html'
    title = "ДСС: подробнее"
    

class ListServiceView(ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'app_services/listservices.html'
        
    def get_queryset(self):
        category = self.kwargs.get('category')
        typesrvc = self.kwargs.get('typesrvc')
        typeservice = get_object_or_404(TypeService, slug=typesrvc)
        services = Service.objects.filter(category=category, typeservice=typeservice.id)
        return services

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('category')
        typesrvc = self.kwargs.get('typesrvc')
        context['category'] = category
        for item in CHOICE_CATEGORY:
            if item[0] == category:
                txt_category = item[1]
                break
        if not txt_category:
            raise Http404
        in_typeservice = get_object_or_404(TypeService, slug=typesrvc)
        context['typeservices'] = TypeService.objects.filter(category=category)
        title = f"ДСС: {txt_category}: {in_typeservice.name}"
        context['title'] = title
        context['currenttype'] = in_typeservice.name
        services = Service.objects.filter(typeservice=in_typeservice.id)
        context['services'] = services
        return context
        
class ListTypeServiceView(TitleMixin, TemplateView):
    '''Показать список услуг сгруппированных по типам в одной из категорий спот, секции, прочие или отдых'''
    template_name = 'app_services/index_category.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('category')
        context['category'] = category
        txt_category = None
        for item in CHOICE_CATEGORY:
            if item[0] == category:
                txt_category = item[1]
                break
        if not txt_category:
            raise Http404
        if category == "other":
            typeservices = TypeService.objects.filter(
                Q(category='relax') | Q(category=category))\
                    .order_by('-order')
            # typeservices += TypeService.objects.filter(category=category).order_by('-order')
        else:
            typeservices = TypeService.objects.filter(category=category).order_by('-order')
        objects_news = News.objects.filter(tags__in=[3])
        context['objects_news'] = objects_news
        context['title'] = f"ДСС: {txt_category}"
        context['typeservices'] = typeservices
        context['categoryname'] = txt_category
        return context
        
    

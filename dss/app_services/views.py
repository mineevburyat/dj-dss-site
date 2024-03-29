from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
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
from app_objects.models import Object
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


class DetailServiceView(TitleMixin, DetailView):
    model = Service
    context_object_name = 'service'
    template_name = 'app_services/detail_new.html'
    title = "ДСС: подробнее"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj'] = self.object.get_object()
        context['categoryname'] = self.object.get_category_name()
        context['categoryslug'] = 'sport'
        context['currenttype'] = self.object.typeservice
        # txt_category = None
        # context['categoryslug'] = category
        # for item in CHOICE_CATEGORY:
        #     if item[0] == category:
        #         txt_category = item[1]
        #         break
        # if not txt_category:
        #     raise Http404
        # in_typeservice = get_object_or_404(TypeService, slug=typesrvc)
        # context['currenttype'] = in_typeservice
        # context['categoryname'] = txt_category
        return context
    
    
#/services/category/servtype (/sport/swimm, /relax/hostel)
class ListServiceView(ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'app_services/listservices_new1.html'
        
    def get_queryset(self):
        # category = self.kwargs.get('category')
        typesrvc = self.kwargs.get('typesrvc')
        # получить услуги этой категории и типу услуг
        typeservice = get_object_or_404(TypeService, slug=typesrvc)
        services = Service.objects.filter(
            typeservice=typeservice.id).order_by('-order')
        return services
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('category')
        typesrvc = self.kwargs.get('typesrvc')
        txt_category = None
        context['categoryslug'] = category
        for item in CHOICE_CATEGORY:
            if item[0] == category:
                txt_category = item[1]
                break
        if not txt_category:
            raise Http404
        in_typeservice = get_object_or_404(TypeService, slug=typesrvc)
        title = f"ДСС: {txt_category}: {in_typeservice.name}"
        context['title'] = title
        context['currenttype'] = in_typeservice
        context['categoryname'] = txt_category
        services = self.get_queryset()
        # собрать словарь: ключь спортплощадка значение список услуг
        areas = set()
        for service in services:
            areas.add(service.sportarea)
        area_servs = {}
        for area in areas:
            for service in services:
                if service.sportarea == area:
                    if area_servs.get(area):
                        area_servs[area].append(service)
                    else:
                        area_servs[area] = [service]
        context['dic_area_srvs'] = area_servs
        
        startDate = timezone.now() - timedelta(days=30)
        endDate = timezone.now() + timedelta(days=30)
        object_news = []
        events = []
        for news in News.objects.filter(date_activation__range=(startDate, endDate)).order_by("-date_activation"):
            if news.is_actual():
                object_news.append(news)
                if news.is_actual():
                    events.append(news)
        if len(events) < 3:
            events.extend(object_news[:3])
        context['objects_news'] = object_news[:6]
        context['events'] = events[:3]
        return context
    
        
# services/category (sport. section, relax, other)
class ListTypeServiceView(TitleMixin, ListView):
    '''Показать список услуг сгруппированных по типам в одной из категорий спот, секции, прочие или отдых'''
    template_name = 'app_services/index_new.html'
    model = TypeService
    context_object_name = 'typeservices'
    title = 'ДСС: услуги'
    
    def get_queryset(self):
        query = super().get_queryset()
        category = self.kwargs.get('category')
        # if category == "other":
        #     query = query.filter(
        #         Q(category='relax') | Q(category=category))\
        #             .order_by('-order')
        #     query += TypeService.objects.filter(category=category).order_by('-order')
        # else:
        query = TypeService.objects.filter(category=category).filter(active=True).order_by('-order')
        return query
    
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
        objects_news = News.objects.filter(tags__in=[3])
        context['objects_news'] = objects_news
        context['title'] = f"ДСС: {txt_category}"
        context['categoryname'] = txt_category
        return context
        
    
def campingview(request):
    template_name = 'app_services/camping.html'
    context = {}
    category = 'relax'
    context['category'] = category
    for item in CHOICE_CATEGORY:
        if item[0] == category:
            txt_category = item[1]
            break
    in_typeservice = get_object_or_404(TypeService, slug='kemping')
    typeservices = [item for item in TypeService.objects.filter(category=category).order_by('-order') if item != in_typeservice]
    param_objcts = request.GET.get('objects')
    if param_objcts:
        param_objcts = param_objcts.split(',')
    else:
        param_objcts = [i.slug for i in Object.objects.all()]
    context['typeservices'] = typeservices
    title = f"ДСС: {txt_category}: Байкал Парк"
    context['title'] = title
    context['currenttype'] = in_typeservice
    context['categoryname'] = txt_category
    services = Service.objects.filter(typeservice=in_typeservice.id)
        # context['services'] = services
    objs = set()
    for service in services:
        objs.add(service.object)
    context['obj_filter'] = objs
    context['param_objs'] = param_objcts
    return render(request, template_name, context)
        
def sectionview(request, **kwargs):
    template_name = 'app_services/section.html'
    section = kwargs.get('section')
    
    context = {}
    category = 'section'
    context['category'] = category
    for item in CHOICE_CATEGORY:
        if item[0] == category:
            txt_category = item[1]
            break
    in_typeservice = get_object_or_404(TypeService, slug=section)
    typeservices = [item for item in TypeService.objects.filter(category=category).order_by('-order') if item != in_typeservice]
    param_objcts = request.GET.get('objects')
    if param_objcts:
        param_objcts = param_objcts.split(',')
    else:
        param_objcts = [i.slug for i in Object.objects.all()]
    context['typeservices'] = typeservices
    title = f"ДСС: {txt_category}: Байкал Парк"
    context['title'] = title
    context['currenttype'] = in_typeservice
    context['categoryname'] = txt_category
    services = Service.objects.filter(typeservice=in_typeservice.id)
        # context['services'] = services
    objs = set()
    for service in services:
        objs.add(service.object)
    context['obj_filter'] = objs
    context['param_objs'] = param_objcts
    return render(request, template_name, context)
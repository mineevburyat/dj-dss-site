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


class DetailServiceView(TitleMixin, DetailView):
    model = Service
    context_object_name = 'service'
    template_name = 'app_services/detail.html'
    title = "ДСС: подробнее"
    
#/services/category/servtype (/sport/swimm, /relax/hostel)
class ListServiceView(ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'app_services/listservices_new.html'
        
    def get_queryset(self):
        category = self.kwargs.get('category')
        typesrvc = self.kwargs.get('typesrvc')
        # param_objcts = self.request.GET.get('objects')
        typeservice = get_object_or_404(TypeService, slug=typesrvc)
        services = Service.objects.filter(category=category, typeservice=typeservice.id).order_by('object', '-order')
        # else:
        #     param_objcts = param_objcts.split(',')
        #     objs = [i.pk for i in Object.objects.filter(slug__in=param_objcts)]
        #     services = Service.objects.filter(category=category, typeservice=typeservice.id, object__in=objs).order_by('object', '-order')
        # print(services)
        return services
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs.get('category')
        typesrvc = self.kwargs.get('typesrvc')
        # param_objcts = self.request.GET.get('objects')
        # if param_objcts:
        #     param_objcts = param_objcts.split(',')
        # else:
        #     param_objcts = [i.slug for i in Object.objects.all()]
        context['categoryslug'] = category
        for item in CHOICE_CATEGORY:
            if item[0] == category:
                txt_category = item[1]
                break
        if not txt_category:
            raise Http404
        in_typeservice = get_object_or_404(TypeService, slug=typesrvc)
        # typeservices = [item for item in TypeService.objects.filter(category=category).order_by('-order') if item != in_typeservice]
        # context['typeservices'] = typeservices
        
        title = f"ДСС: {txt_category}: {in_typeservice.name}"
        context['title'] = title
        context['currenttype'] = in_typeservice
        context['categoryname'] = txt_category
        services = self.get_queryset()
        areas = set()
        for service in services:
            areas.add(service.sportarea)
        # context['obj_filter'] = objs
        # print(objs)
        area_servs = {}
        for area in areas:
            for service in services:
                if service.sportarea == area:
                    if area_servs.get(area):
                        area_servs[area].append(service)
                    else:
                        area_servs[area] = [service]
        print(area_servs)
                    
        context['dic_area_srvs'] = area_servs
        return context
    
    # def get(self, request, *args, **kwargs):
    #     lastslugurl = request.path.split('/')[-1]
    #     secondslugurl = request.path.split('/')[-2]
    #     # if lastslugurl == 'kemping':
    #     #     return redirect('/services/camping')
    #     # if secondslugurl == 'section':
    #     #     return redirect(reverse('services:hardsection', kwargs={'section': lastslugurl}))
    #     return super().get(request, *args, **kwargs)
        
    # def get_queryset(self):
    #     category = self.kwargs.get('category')
    #     typesrvc = self.kwargs.get('typesrvc')
    #     param_objcts = self.request.GET.get('objects')
    #     typeservice = get_object_or_404(TypeService, slug=typesrvc)
    #     if param_objcts is None:
    #         services = Service.objects.filter(category=category, typeservice=typeservice.id).order_by('object', '-order')
    #     else:
    #         param_objcts = param_objcts.split(',')
    #         objs = [i.pk for i in Object.objects.filter(slug__in=param_objcts)]
    #         services = Service.objects.filter(category=category, typeservice=typeservice.id, object__in=objs).order_by('object', '-order')
    #     return services

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     category = self.kwargs.get('category')
    #     typesrvc = self.kwargs.get('typesrvc')
    #     param_objcts = self.request.GET.get('objects')
    #     if param_objcts:
    #         param_objcts = param_objcts.split(',')
    #     else:
    #         param_objcts = [i.slug for i in Object.objects.all()]
    #     context['category'] = category
    #     for item in CHOICE_CATEGORY:
    #         if item[0] == category:
    #             txt_category = item[1]
    #             break
    #     if not txt_category:
    #         raise Http404
    #     in_typeservice = get_object_or_404(TypeService, slug=typesrvc)
    #     typeservices = [item for item in TypeService.objects.filter(category=category).order_by('-order') if item != in_typeservice]
    #     context['typeservices'] = typeservices
        
    #     title = f"ДСС: {txt_category}: {in_typeservice.name}"
    #     context['title'] = title
    #     context['currenttype'] = in_typeservice
    #     context['categoryname'] = txt_category
    #     services = Service.objects.filter(typeservice=in_typeservice.id)
    #     # context['services'] = services
    #     objs = set()
    #     for service in services:
    #         objs.add(service.object)
    #     context['obj_filter'] = objs
    #     context['param_objs'] = param_objcts
    #     return context
        
# services/category (sport. section, relax, other)
class ListTypeServiceView(TitleMixin, ListView):
    '''Показать список услуг сгруппированных по типам в одной из категорий спот, секции, прочие или отдых'''
    template_name = 'app_services/index_new.html'
    model = TypeService
    context_object_name = 'typeservices'
    title = 'ДСС: услуги'
    
    def get_queryset(self):
        query = super().get_queryset()
        print(query)
        category = self.kwargs.get('category')
        if category == "other":
            query = query.filter(
                Q(category='relax') | Q(category=category))\
                    .order_by('-order')
            query += TypeService.objects.filter(category=category).order_by('-order')
        else:
            query = TypeService.objects.filter(category=category).filter(active=True).order_by('-order')
        print(query)
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
        # if category == "other":
        #     typeservices = TypeService.objects.filter(
        #         Q(category='relax') | Q(category=category))\
        #             .order_by('-order')
        #     # typeservices += TypeService.objects.filter(category=category).order_by('-order')
        # else:
        # typeservices = TypeService.objects.filter(category=category).filter(active=True).order_by('-order')
        objects_news = News.objects.filter(tags__in=[3])
        context['objects_news'] = objects_news
        context['title'] = f"ДСС: {txt_category}"
        # context['typeservices'] = typeservices
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
    print(request)
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
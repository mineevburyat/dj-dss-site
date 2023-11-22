from django.views.generic.base import TemplateView
from common.mixins import TitleMixin, ObjectsMixin
from .models import Object, ObjectGallery, SportArea
from app_services.models import Service
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from app_news.models import News
from calendar import Calendar
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from app_tags.models import Tag
from django.utils import timezone

def name_of_week(day):
    return ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье'][day]

def name_of_month(month):
    return ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'][month-1]

class IndexView(TitleMixin, TemplateView):
    template_name = 'app_objects/index.html'
    title = "ДСС:объекты"
    

class DetailObjectView(TitleMixin, ObjectsMixin, DetailView):
    model = Object
    context_object_name = 'object'
    template_name = 'app_objects/detail.html'
    title = "ДСС: о спортобъекте"
    # objects = Object.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        id = obj.pk
        tags = Tag.objects.filter(tag__in=[obj.short_name, 'новость'])
        context['object_id'] = id
        
        # вытащить новости и важные события связанные с конкретным объектом
        startDate = timezone.now() - timedelta(days=30)
        endDate = timezone.now() + timedelta(days=30)
        object_news = []
        events = []
        for news in News.objects.filter(date_activation__range=(startDate, endDate)).order_by("-date_activation"):
            if news.valid_until_date > timezone.now():
                continue
            if news.important:
                events.append(news)
            object_news.append(news)    
        
        context['objects_news'] = object_news[:6]
        context['events'] = events[:3]
        # context['services'] = self.object.services.filter(object=self.object.pk).order_by('order')
        return context

class ListObjectsView(TitleMixin, ListView):
    model = Object
    context_object_name = 'objects'
    template_name = 'app_objects/index.html'
    ordering = ['-order']
    title = "ДСС: список объектов"
    
    def get_queryset(self):
        objects = Object.objects.all().order_by('-order')
        return objects
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objects_news = News.objects.filter(tags__in=[2])
        context['objects_news'] = objects_news[:3]
        return context
    
class DetailAreaView(TitleMixin, DetailView):
    model = SportArea
    context_object_name = 'area'
    template_name = 'app_objects/area.html'
    title = "ДСС: спортплощадка"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_slug = self.kwargs.get('obj_slug')
        object = get_object_or_404(Object, slug=obj_slug)
        context['object'] = object
        tags = Tag.objects.filter(tag__in=[object.short_name, 'новость'])
        startDate = timezone.now() - timedelta(days=30)
        endDate = timezone.now() + timedelta(days=30)
        object_news = []
        events = []
        for news in News.objects.filter(date_activation__range=(startDate, endDate)).order_by("-date_activation"):
            if news.valid_until_date > timezone.now():
                continue
            if news.important:
                events.append(news)
            object_news.append(news)
        context['objects_news'] = object_news[:6]
        context['events'] = events[:3]
        return context
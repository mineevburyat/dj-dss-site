from django.views.generic.base import TemplateView
from common.mixins import TitleMixin, ObjectsMixin
from .models import Object, ObjectGallery, SportArea
from app_services.models import Service
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from app_news.models import News
from calendar import Calendar
from datetime import datetime
from django.shortcuts import get_object_or_404

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
    objects = Object.objects.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.object.pk
        gallery = ObjectGallery.objects.filter(obj=id)
        photos = []
        for photo in gallery:
            photos.append(photo.photos)
        context['object_id'] = id
        context['photos'] = photos
        # вытащить новости и важные события связанные с конкретным объектом
        objects_news = News.objects.filter(tags__in=[id])
        # calendar = Calendar()
        # days = []
        # now = datetime.now()
        # for day in calendar.itermonthdays2(now.year, now.month):
        #     days.append(day[0])
        # context['days'] = days
        # context['today'] = (now, name_of_month(now.month), name_of_week(now.weekday()))
        # context['events'] = {25:"особое событие 1", 30:"особое событие 2"}
        context['objects_news'] = objects_news
        context['services'] = self.object.services.filter(object=self.object.pk).order_by('order')
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
    
    
    # def get_queryset(self):
    #     category = self.kwargs.get('category')
    #     if category:
    #         services = Object.objects.filter(category=category)
    #     else:
    #         services = Object.objects.all()
    #     return services

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
        objects_news = News.objects.filter(tags__in=[self.object.obj.pk])
        context['area_news'] = objects_news
        # print(obj_slug, context['object'])
        # context['object'] = Object.objects.get(slug=obj_slug)
        # id = self.object.pk
        # gallery = ObjectGallery.objects.filter(obj=id)
        # photos = []
        # for photo in gallery:
        #     photos.append(photo.photos)
        # context['object_id'] = id
        # context['photos'] = photos
        # # вытащить новости и важные события связанные с конкретным объектом
        # 
        # calendar = Calendar()
        # days = []
        # now = datetime.now()
        # for day in calendar.itermonthdays2(now.year, now.month):
        #     days.append(day[0])
        # context['days'] = days
        # context['today'] = (now, name_of_month(now.month), name_of_week(now.weekday()))
        # context['objects_news'] = objects_news
        # context['events'] = {25:"особое событие 1", 30:"особое событие 2"}
        # context['services'] = self.object.services.filter(object=self.object.pk).order_by('order')
        # self.object.typestock
        return context
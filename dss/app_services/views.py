from typing import Any, Dict, Optional

from django.shortcuts import get_object_or_404
from django.db import models
from .models import Service
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from common.mixins import TitleMixin
# from common.mixins import TitleMixin


class DetailServiceView(TitleMixin, DetailView):
    model = Service
    context_object_name = 'service'
    template_name = 'app_services/detail.html'
    title = "ДСС: подробнее"
    

class ListServiceView(TitleMixin, ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'app_services/list.html'
    title = "ДСС: список"
    
    def get_queryset(self):
        category = self.kwargs.get('category')
        if category:
            services = Service.objects.filter(category=category)
        else:
            services = Service.objects.all()
        return services

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        return context
        
    

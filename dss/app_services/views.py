from typing import Any, Dict, Optional

from django.shortcuts import get_object_or_404
from django.db import models
from .models import Service
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
# from common.mixins import TitleMixin


class ServiceViewByCategory(TemplateView):
    template_name = 'app_services/index_category.html'
    # title = "Магазин Store - главная"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        return context
    
class DetailService(DetailView):
    model = Service
    context_object_name = 'service'
    template_name = 'app_services/detail.html'
    # title = "Магазин Store - главная"
    

class ListService(ListView):
    model = Service
    context_object_name = 'services'
    template_name = 'app_services/list.html'
    

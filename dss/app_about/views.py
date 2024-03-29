from typing import Any
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from .models import Manager, Vacant, Document
# from common.mixins import TitleMixin
from app_contacts.models import Contact


class IndexView(TemplateView):
    template_name = 'app_about/index.html'
    # title = "Магазин Store - главная"
    
class ManagmentView(ListView):
    template_name = 'app_about/managment.html'
    model = Manager
    context_object_name = 'pipls'
    
class DTurView(TemplateView):
    template_name = 'app_about/3dtur.html'
    
class DocumentsView(TemplateView, ):
    template_name = 'app_about/documents.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['dic_documents'] = Document.objects.dic_documents()
        return context
    
class ContactsView(TemplateView):
    template_name = 'app_about/contacts.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['contacts'] = Contact.objects.dic_object_contacts()
        return context
    
    
class VacantView(TemplateView):
    template_name = 'app_about/jobs.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['obj_vacants_dic'] = Vacant.objects.dic_object_vacants()
        return context
    
class ZakupsView(TemplateView):
    template_name = 'app_about/purchases.html'
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['purchases'] = Document.objects.only_purchases()
        return context
    
class ReseptionView(TemplateView):
    template_name = 'app_about/reseption.html'
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from .models import Manager
# from common.mixins import TitleMixin


class IndexView(TemplateView):
    template_name = 'app_about/index.html'
    # title = "Магазин Store - главная"
    
class ManagmentView(ListView):
    template_name = 'app_about/managment.html'
    model = Manager
    context_object_name = 'pipls'
    
class DTurView(TemplateView):
    template_name = 'app_about/3dtur.html'
    
class DocumentsView(TemplateView):
    template_name = 'app_about/documents.html'
    
class ContactsView(TemplateView):
    template_name = 'app_about/contacts.html'
    
class VacantView(TemplateView):
    template_name = 'app_about/jobs.html'
    
class ZakupsView(TemplateView):
    template_name = 'app_about/purchases.html'
    
class ReseptionView(TemplateView):
    template_name = 'app_about/reseption.html'
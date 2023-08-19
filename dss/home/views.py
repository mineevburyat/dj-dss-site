from django.views.generic.base import TemplateView
from common.mixins import TitleMixin, ObjectsMixin
from app_objects.models import Object
from app_services.models import TypeService


class IndexView(TitleMixin, ObjectsMixin, TemplateView):
    template_name = 'home/index_dep.html'
    title = "главная"
    objects = Object.objects.all().order_by('-order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sportservices'] = TypeService.objects\
            .filter(category='sport')\
            .filter(active=True)\
            .order_by('-order')
        context['relaxservices'] = TypeService.objects.filter(category='relax').order_by('-order')
        return context
    

from django.views.generic.base import TemplateView
from common.mixins import TitleMixin, ObjectsMixin
from app_objects.models import Object


class IndexView(TitleMixin, ObjectsMixin, TemplateView):
    template_name = 'home/index.html'
    title = "ДСС - дирекция спортивных сооружений"
    objects = Object.objects.all()

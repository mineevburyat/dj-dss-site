from django.views.generic.base import TemplateView
from common.mixins import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name = 'app_objects/index.html'
    title = "ДСС:объекты"
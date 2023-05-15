from django.views.generic.base import TemplateView
from common.mixins import TitleMixin


class IndexView(TitleMixin, TemplateView):
    template_name = 'home/index.html'
    title = "ДСС - дирекция спортивных сооружений"

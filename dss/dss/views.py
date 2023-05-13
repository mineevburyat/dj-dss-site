from django.views.generic.base import TemplateView
# from common.mixins import TitleMixin


class IndexView(TemplateView):
    template_name = 'index.html'
    # title = "Магазин Store - главная"
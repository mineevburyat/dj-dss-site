from django.views.generic.base import TemplateView
# from common.mixins import TitleMixin


class IndexView(TemplateView):
    template_name = 'app_about/index.html'
    # title = "Магазин Store - главная"
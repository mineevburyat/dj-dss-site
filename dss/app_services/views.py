from django.views.generic.base import TemplateView
# from common.mixins import TitleMixin


class IndexView(TemplateView):
    template_name = 'app_services/index.html'
    # title = "Магазин Store - главная"
    
class ServiceViewByCategory(TemplateView):
    template_name = 'app_services/index_category.html'
    # title = "Магазин Store - главная"
    
class SportSectionView(TemplateView):
    template_name = 'app_services/index.html'
    # title = "Магазин Store - главная"
    
class OtherServiceView(TemplateView):
    template_name = 'app_services/index.html'
    # title = "Магазин Store - главная"
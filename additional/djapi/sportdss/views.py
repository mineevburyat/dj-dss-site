from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View
from .models import BaseCategory, Service, About, Object


# def get_lst_category(category):
#     if category == 2 or category == 259 or category == 299:
#         lst = [item for item in Service.objects.all() if item.category.id == category]
#     elif category == 335:
#         lst = [item for item in About.objects.all()]
#     elif category == 7632:
#         lst = [item for item in Object.objects.all()]
#     else:
#         lst = []
#     return lst
# def home(request):
#     return HttpResponse("Гланая страница dss-sport")

class Home(View):
    def get(self, request, *args, **kwargs):
        mainmenu = BaseCategory.objects.all()
        for menu in mainmenu:
            if menu.id == 2:
                sports = menu.get_submenu()
            elif menu.id == 259:
                sections = menu.get_submenu()
            elif menu.id == 299:
                otherservices = menu.get_submenu()
            elif menu.id == 335:
                abouts = menu.get_submenu()
            elif menu.id == 7632:
                objects = menu.get_submenu()
        return render(
            request, 
            'home.html', 
            context={
                'mainmenu': mainmenu,
                'sportservices': sports,
                'otherservices': otherservices,
                'sections': sections,
                'abouts': abouts,
                'objects': objects
                }
            )
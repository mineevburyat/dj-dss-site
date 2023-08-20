from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def lk_view(request):
    template_name = 'app_lk/index.html'
    context = {}
    return render(request, template_name, context)

def shedule_view(request):
    template_name = 'app_lk/shedule_1c.html'
    context = {}
    return render(request, template_name, context)
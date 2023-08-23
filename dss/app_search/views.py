from django.shortcuts import render
from django.db.models import Q
from app_news.models import News
from app_services.models import Service

# Create your views here.
def result(request):
    template = 'app_search/index.html'
    find_str = request.GET.get('search')
    news_result = News.objects.filter(
        Q(content__icontains=find_str) | Q(title__icontains=find_str))
    context = {}
    context['news_results'] = news_result
    context['find_str'] = find_str
    service_result = Service.objects.filter(
        Q(description__icontains=find_str) | Q(name__icontains=find_str))
    context['service_results'] = service_result
    return render(request, template, context)
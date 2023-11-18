from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from .models import News

class NewsListView(ListView):
    template_name = 'app_news/index_new.html'
    paginate_by = 10
    model = News
    context_object_name = 'news_list'
    ordering = ('-pk',)
        
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        current_page = kwargs.get("page", 1)
        page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number, on_each_side=1, on_ends=1)
        return context
    
class NewsDetailView(DetailView):
    model = News
    template_name = 'app_news/detail.html'
    context_object_name = 'news'
    
    

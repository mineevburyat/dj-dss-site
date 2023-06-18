from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView
from .models import ImageMedia
from .forms import ImageForm
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy, reverse

# Create your views here.


class ImageGalleryView(ListView):
    template_name = 'app_news/base.html'
    paginate_by = 8
    model = ImageMedia
    context_object_name = 'images'
    ordering = ('pk',)
        
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        curent_page = kwargs.get("page", 1)
        page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(page.number, on_each_side=1, on_ends=1)
        return context
    
class ImageDetailView(DetailView):
    model = ImageMedia
    template_name = 'app_news/detail_img.html'
    context_object_name = 'image'
    
    
class ImageEditForm(UpdateView):
    model = ImageMedia
    fields = ['slug', 'title', 'caption', 'alt_txt']
    template_name = 'app_news/edit_img.html'
    context_object_name = 'image'
    
class ImageDeleteForm(DeleteView):
    model = ImageMedia
    template_name = 'app_news/delete_img.html'
    
    def get_success_url(self) -> str:
        return reverse('app_news:detailimg', kwargs = {
                     'slug': self.object.get_next_slug()})
    

    
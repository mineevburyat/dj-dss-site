from django.contrib import admin
from .models import Service
from django.db import models
from django.forms import TextInput

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('icon_html_img', 'name', 'category', 'slug', 'photo')
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    }
    prepopulated_fields = {"slug": ("name",)}
    fields = ['category', 
              ('name', 'slug'), 
              'description', 
              ('icon_html_img', 'icon'),
              ('photo_html_img', 'photo')]
    readonly_fields = ('icon_html_img', 'photo_html_img')
    def get_form(self, request, obj=None, **kwargs):
        form = super(ServiceAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 40em;'
        return form
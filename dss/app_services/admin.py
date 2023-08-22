from django.contrib import admin
from .models import Service, VariousSport, TypeService, TypeServiceGallery
from django.db import models
from django.forms import TextInput

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_typestock', 'typeservice')
    ordering = ('object', 'category', 'typeservice', '-order')
    list_display_links = ('name',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    }
    prepopulated_fields = {"slug": ("name",)}
    fields = [('category', 'typeservice', 'object', 'typestock'),
              ('name', 'slug', 'order'), 
              'description', 
            ]
    list_filter = ('category', 'typeservice', 'object')
    
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ServiceAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 40em;'
        return form
    
@admin.register(VariousSport)
class VariousSportAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name', 'slug')
    ordering = ('pk',)


@admin.register(TypeService)
class TypeServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'order', 'get_typestock_name', 'active', 'icon_html_img')
    ordering = ('-category', '-order')
    list_editable = ('order', 'active')
    fields = (
        ('name', 'slug', 'category'),
        ('order', 'icon'),
        ('description', 'typestock'),
        ('icon_html_img', 'active')
    )
    readonly_fields = ('icon_html_img',)
    
    
@admin.register(TypeServiceGallery)
class TypeServiceGalleryAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_html_photo', 'get_img_size')
    list_filter = ('typeservice',)
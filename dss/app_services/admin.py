from django.contrib import admin
from .models import (Service,
                     TypeService,
                     TypeServiceGallery,
                     Rate,
                     Discount,
                     Promotion)
from django.db import models
from django.forms import TextInput
from django.template.loader import get_template
from django_ace import AceWidget


class RateInline(admin.TabularInline):
    model = Rate
    extra = 0
    

class DiscontInline(admin.TabularInline):
    model = Discount
    extra = 0
    list_display_links = ('__str__',)
    
    

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_obj_name')
    ordering = ('typeservice', '-order')
    list_display_links = ('__str__',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    }
    prepopulated_fields = {"slug": ("name",)}
    fields = [('typeservice', 'sportarea'),
              ('name', 'slug', 'order'), 
              'description', 
            ]
    list_filter = ('sportarea', 'typeservice')
    inlines = [RateInline]
    
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ServiceAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 40em;'
        return form


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    inlines = [DiscontInline]
    list_filter = ('service',)
class PromotionInline(admin.StackedInline):
    model = Promotion
    extra = 0
    
@admin.register(TypeService)
class TypeServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'order', 'active', 'icon_html_img', 'get_count_services', 'get_count_photos')
    ordering = ('-category', '-order')
    list_editable = ('order', 'active')
    fields = (
        ('name', 'slug', 'category'),
        ('order', 'icon'),
        ('description', ),
        ('icon_html_img', 'active')
    )
    readonly_fields = ('icon_html_img',)
    
    
@admin.register(TypeServiceGallery)
class TypeServiceGalleryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_count_photo')
    readonly_fields = ('get_count_photo', )
    # list_filter = ('typeservice',)
    filter_horizontal = ('photos',)
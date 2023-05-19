from django.contrib import admin
from django.db import models
from django.forms import TextInput
from .models import Object, Subunit, TypeStock
# Register your models here.

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'slug', 'icon_html_img', 'order')
    # ordering = ('order',)
    readonly_fields = ('icon_html_img',)
    prepopulated_fields = {"slug": ("short_name",)}
    fields = [('short_name', 'slug', 'order'),
              'name', 'address', 'description',
              ('icon', 'photo')]
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    }
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ObjectAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 50em;'
        form.base_fields['address'].widget.attrs['style'] = 'width: 50em;'
        return form

    
@admin.register(TypeStock)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon_html_img', 'order')
    ordering = ('order','pk')
    readonly_fields = ('icon_html_img',)
    prepopulated_fields = {"slug": ("name",)}
    fields = [('name', 'slug', 'order'),
              ('icon_html_img','icon')]

@admin.register(Subunit)
class SubunitAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'obj')
    prepopulated_fields = {"slug": ("name",)}
    # fields = [('short_name', 'slug'), 'name', 'address', 'description', ('icon', 'photo')]
    # formfield_overrides = {
    #     models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    # }
    
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(ObjectAdmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields['name'].widget.attrs['style'] = 'width: 50em;'
    #     form.base_fields['address'].widget.attrs['style'] = 'width: 50em;'
    #     return form
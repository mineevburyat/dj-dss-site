from django.contrib import admin
from django.db import models
from django.forms import TextInput
from .models import Object, SportArea,  ObjectGallery
# Register your models here.

class SportAreaInline(admin.StackedInline):
    model = SportArea
    extra = 0

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'slug', 'icon_html_img', 'order')
    ordering = ('-order',)
    readonly_fields = ('icon_html_img', 'get_icon_url')
    prepopulated_fields = {"slug": ("short_name",)}
    # fields = [('short_name', 'slug', 'order'),
    #           ('name', 'icon_lib'),
    #           ('address', 'icon_html_img'),
    #           'description',
    #           ]
    fieldsets = (
        (None, {'fields': [
            ('short_name', 'slug', 'order'),
            ('name', 'icon_lib'),
            ('address', 'icon_html_img'),
            'description',
              ]}),
        ('характеристики', {'fields': ('start_date', 'square')}),
        ('контакты', {'fields': ('call_center',)})
    )
    # filter_horizontal = ('type_stock',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    }
    inlines = [SportAreaInline]
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ObjectAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 50em;'
        form.base_fields['address'].widget.attrs['style'] = 'width: 50em;'
        return form

    
@admin.register(SportArea)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'obj', 'order')
    ordering = ('obj', 'order')
    readonly_fields = ('icon_html_img',)
    prepopulated_fields = {"slug": ("name",)}
    fields = [('name', 'slug', 'order', 'obj'),
              ('icon_html_img', 'icon'),
              ('description', 'inviting_mes'),
              'characteristics']
    list_filter = ('obj',)

# @admin.register(Subunit)
# class SubunitAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug', 'obj')
#     prepopulated_fields = {"slug": ("name",)}
    # fields = [('short_name', 'slug'), 'name', 'address', 'description', ('icon', 'photo')]
    # formfield_overrides = {
    #     models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    # }
    
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(ObjectAdmin, self).get_form(request, obj, **kwargs)
    #     form.base_fields['name'].widget.attrs['style'] = 'width: 50em;'
    #     form.base_fields['address'].widget.attrs['style'] = 'width: 50em;'
    #     return form
    
# @admin.register(ObjectPhoto)
# class OblectsPhotoAdmin(admin.ModelAdmin):
#     list_display = ('obj', )
    
    
@admin.register(ObjectGallery)
class OblectGalleryAdmin(admin.ModelAdmin):
    list_display = ('get_short_name', 'get_html_photo', 'get_img_size')
    list_filter = ('obj',)
    fields = ['obj', 'area', 'photos', 'get_html_photo']
    readonly_fields = ('get_html_photo',)
    
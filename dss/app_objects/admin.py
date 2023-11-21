from django.contrib import admin
from django.db import models
from django.forms import TextInput
from .models import (Object,
                     SportArea,
                     ObjectGallery,
                     SportAreaGallery)
from django import forms

# Register your models here.

class SportAreaInline(admin.StackedInline):
    model = SportArea
    extra = 0
    fieldsets = (
        ('Название и описание', {'fields': [
            ('name', 'slug', 'order'),
            ('obj', 'icon'),
            'inviting_mes',
            'description',
            ]}),
        ('характеристики', {'fields': (
            'characteristics',)
            }),
        )

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'slug', 'get_num_areas', 'icon_html_img', 'order')
    ordering = ('-order',)
    readonly_fields = ('icon_html_img', 'get_icon_url')
    prepopulated_fields = {"slug": ("short_name",)}
    fieldsets = (
        ('Название и описание', {'fields': [
            ('short_name', 'slug', 'order'),
            ('name', 'address'),
            ('icon_lib', 'icon_html_img'),
            'description',
              ]}),
        ('характеристики', {'fields': (
            'start_date',
             'square')
                            }),
        ('контакты', {'fields': (
            'call_center',)
                      })
    )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
    }
    inlines = [SportAreaInline]
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(ObjectAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 50em;'
        form.base_fields['address'].widget.attrs['style'] = 'width: 50em;'
        return form

class SportAreaForm(forms.ModelForm):
    class Meta:
        model = SportArea
        fields = "__all__"
        readonly_fields = ('icon_html_img',)
        prepopulated_fields = {"slug": ("name",)}
        list_filter = ('obj',)
        fieldsets = (
            ('Название и описание', {'fields': [
                ('name', 'slug', 'order'),
                ('obj', 'icon', 'icon_html_img'),
                'inviting_mes',
                'description',
            ]}),
            ('характеристики', {'fields': (
                'characteristics',)
            }),
        )
        widgets = {
            'characteristics': forms.Textarea(attrs={'class': 'json-editor'})
        }
@admin.register(SportArea)
class SportAreaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slug', 'order')
    ordering = ('obj', '-order')
    readonly_fields = ('icon_html_img',)
    form = SportAreaForm
    # prepopulated_fields = {"slug": ("name",)}
    # list_filter = ('obj',)
    # fieldsets = (
    #     ('Название и описание', {'fields': [
    #         ('name', 'slug', 'order'),
    #         ('obj', 'icon', 'icon_html_img'),
    #         'inviting_mes',
    #         'description',
    #         ]}),
    #     ('характеристики', {'fields': (
    #         'characteristics',)
    #         }),
    #     )

@admin.register(ObjectGallery)
class OblectGalleryAdmin(admin.ModelAdmin):
    list_display = ('get_short_name', 'get_count_photos')
    list_filter = ('obj',)
    fields = ['obj', 'photos']
    readonly_fields = ('get_short_name', 'get_count_photos')
    filter_horizontal = ('photos',)
    
    

@admin.register(SportAreaGallery)
class SportAreaGalleryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_html_photo', 'get_img_size')
    # list_filter = ('obj',)
    fields = ['sportarea', 'photos', 'get_html_photo']
    readonly_fields = ('get_html_photo',)
    
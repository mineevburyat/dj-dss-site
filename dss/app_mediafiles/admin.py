from django.contrib import admin
from .models import Icon, Tag, Image

# Register your models here.
    
@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_html_img', 'img_size')
    readonly_fields = ('img_size', 'icon_html_img')
    save_on_top = True
    fields = (
        ('icon_html_img', 'image', ),
        ('name', 'img_size')
    )
 
# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
#     search_fields = ["title", "caption"]
#     list_display = ["title", "caption", "img_size", 
#                     "thumbnail_html", "date_public"]
#     readonly_fields = ('img_size', 'photo_img',
#                        'thumbnail_html', 'date_public',
#                        'get_path_forigin', 'get_path_fmedium',
#                        'get_path_fsmall')
#     # list_filter = ["tags"]
#     fields = (
#         ('photo_img', 'img_size'),
#         ('title', 'caption', 'image'),
#         'tags',
#         ('get_path_forigin', 'get_path_fmedium', 'get_path_fsmall', 'date_public')
#     )
#     list_filter = ('tags',)
#     filter_horizontal = ('tags',)

@admin.register(Image)
class AdminImageMedia(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'get_img_size', 
                    'get_fsize', 'thumbnail_html', 'tags_list')
    fieldsets = (
        ('Изображение', {
            'fields': (
                'photo_img',
                ('date_public', 'img_file_size',
                 'get_img_size', 'img_mode', 'media_type'),
                'image',
                ('get_large_html', 'get_medium_html', 'get_small_html')
            )
        }),
        ('Описание', {
            'fields': (
                ('title', 'slug', 'alt_txt'),
                'caption'
            )
        }),
        ('метки', {
            'fields': (
                'tags',
            )
        })
    )
    readonly_fields = ('get_img_size', 'is_caption',
                       'date_public', 'img_file_size', 'img_mode',
                       'media_type', 'get_fsize', 'get_large_html', 'get_medium_html',
                       'get_small_html', 'tags_list', 'photo_img')
    ordering = ('-img_file_size',)
    list_filter = ('tags',)
    filter_horizontal = ('tags',)
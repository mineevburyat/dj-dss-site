from django.contrib import admin
from .models import Icon, Tag, Image

# Register your models here.
    
@admin.register(Icon)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_html_img', 'img_size')
    readonly_fields = ('img_size', 'icon_html_img')
    save_on_top = True
    fields = (
        ('icon_html_img', 'image', ),
        ('name', 'img_size')
    )
 
@admin.register(Tag)   
class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ["name", "description"]
    list_display = ["name", "description", "img_size", 
                    "thumbnail_html", "created"]
    readonly_fields = ('img_size', 'photo_img',
                       'thumbnail_html', 'created',
                       'get_path_forigin', 'get_path_fmedium',
                       'get_path_fsmall')
    # list_filter = ["tags"]
    fields = (
        ('photo_img', 'img_size', 'created'),
        ('name', 'description', 'image'),
        ('get_path_forigin', 'get_path_fmedium', 'get_path_fsmall')
    )

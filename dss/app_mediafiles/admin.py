from django.contrib import admin
from .models import Icon, Tag, Image

# Register your models here.
    
@admin.register(Icon)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_html_img', 'img_size')
    save_on_top = True
 
@admin.register(Tag)   
class TagAdmin(admin.ModelAdmin):
    list_display = ["tag"]

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ["__str__", "name", "description", "img_size", "tags_", "get_thumbnail_html", "created"]
    # list_filter = ["tags"]

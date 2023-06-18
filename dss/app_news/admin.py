from django.contrib import admin
from .models import News, ImageMedia

# Register your models here.
@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_public', 'slug', 'get_thumbnail')
    
@admin.register(ImageMedia)
class AdminImageMedia(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_img_size', 'get_fsize', 'is_caption')
    fields = (
        ('title', 'slug'),
        ('caption', 'alt_txt'),
        'image',
        ('date_public', 'img_file_size', 
         'get_img_size', 'img_mode', 'media_type'),
        ('get_large_html', 'get_medium_html', 'get_small_html')
        
    )
    readonly_fields = ('get_img_size', 'is_caption',
                       'date_public', 'img_file_size', 'img_mode',
                       'width', 'height', 'media_type',
                       'get_fsize', 'get_large_html', 'get_medium_html', 'get_small_html')
    ordering = ('-img_file_size',)
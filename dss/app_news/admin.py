from django.contrib import admin
from .models import News

# Register your models here.
@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_public', 'slug', 'get_thumbnail')
    

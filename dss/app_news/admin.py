from django.contrib import admin
from .models import News

# Register your models here.
@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ('title', 'date_activation', 'important', 'valid_until_date', 'tags_list','get_thumbnail')
    list_filter = ('tags', 'important')
    filter_horizontal = ('tags',)
    ordering = ('-important', '-date_activation')

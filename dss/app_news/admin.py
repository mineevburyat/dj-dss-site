from django.contrib import admin
from .models import News

# Register your models here.
@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ('__str__', 'date_activation', 'important', 'tags_list','get_thumbnail')
    list_filter = ('tags', 'important')
    filter_horizontal = ('tags',)
    ordering = ('-date_activation', '-important',)
    fieldsets = (
        ('Новость', {
            'fields': (
                ('title', 'slug'),
                ('excerpt', 'content',),
                'featured_media'
            )
        }),
        ('Даты и важность', {
            'fields': (
                ('date_public', 'date_activation', 'valid_until_date'),
                ('important', 'level_importance')
            )
        }),
        ('метки', {
            'fields': (
                'tags',
            )
        })
    )
    search_fields = ['content', 'title', 'excerpt']
    date_hierarchy = "valid_until_date"
    readonly_fields = ('date_public',)
    prepopulated_fields = {"slug": ("title",)}

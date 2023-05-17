from django.contrib import admin
from .models import Icon

# Register your models here.
    
@admin.register(Icon)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('icon_html_card',)
    save_on_top = True
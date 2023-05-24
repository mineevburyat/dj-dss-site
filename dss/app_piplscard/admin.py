from django.contrib import admin
from .models import Piple
from app_mediafiles.models import Image

# Register your models here.
@admin.register(Piple)
class PipleAdmin(admin.ModelAdmin):
    list_display = ('fullname', 'get_thumbnail_html')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "photo":
            kwargs["queryset"] = Image.objects.filter(tags=1)
        return super(PipleAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
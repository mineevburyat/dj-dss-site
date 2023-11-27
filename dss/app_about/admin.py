from django.contrib import admin
from .models import Manager
from app_mediafiles.models import Image
# Register your models here.


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ManagerAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['photo'].queryset = Image.objects.filter(tags__in=[24])
        return form
        
from django.contrib import admin
from .models import Manager, Vacant, Document, TypeDocument
from app_mediafiles.models import Image
# Register your models here.


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(ManagerAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['photo'].queryset = Image.objects.filter(tags__in=[24])
        return form
        
        
@admin.register(Vacant)
class VacantAdmin(admin.ModelAdmin):
    pass

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    fields = ('typedoc', ('name', 'file'))
    list_filter = ('typedoc',)
    
@admin.register(TypeDocument)
class DocumentAdmin(admin.ModelAdmin):
    pass
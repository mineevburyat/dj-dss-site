from django.contrib import admin
from .models import Manager, Vacant, Document, TypeDocument, WP_Page
from app_mediafiles.models import Image
from django.contrib.admin import SimpleListFilter
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

class AreaFilter(SimpleListFilter):
    title = 'родители'
    parameter_name = 'parents'
    def lookups(self, request, model_admin):
        objs = set([(item.slug, item.short_name) for item in Object.objects.all()])
        return objs

    def queryset(self, request, queryset):
        if self.value():
            obj = Object.objects.get(slug=self.value())
            area = SportArea.objects.filter(obj=obj)
            return queryset.filter(sportarea__in=area)
        return queryset

@admin.register(WP_Page)
class PagesAdmin(admin.ModelAdmin):
    ordering = ('pk', )
    list_filter = ('template', )
    readonly_fields = ('slug', 'template', 'old_link', 'date', 'title', 'content', 'excerpt', 'parent')
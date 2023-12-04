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
    fields = ('typedoc', ('name', 'file'), ('old_url', 'old_file_name', 'content_type'))
    list_filter = ('typedoc',)
    readonly_fields = ('old_url', 'old_file_name', 'content_type')
    
@admin.register(TypeDocument)
class DocumentAdmin(admin.ModelAdmin):
    pass

class PageFilter(SimpleListFilter):
    title = 'родители'
    parameter_name = 'parents'
    def lookups(self, request, model_admin):
        all = WP_Page.objects.all()
        rel_pages = []
        for item in all:
            if item.wp_page_set.all():
                rel_pages.append(item)
        objs = set([(item.slug, item.title) for item in rel_pages])
        return objs

    def queryset(self, request, queryset):
        if self.value():
            parent = WP_Page.objects.get(slug=self.value())
            return queryset.filter(parent=parent)
        return queryset

@admin.register(WP_Page)
class PagesAdmin(admin.ModelAdmin):
    ordering = ('pk', )
    list_filter = ('template', PageFilter)
    readonly_fields = ('template', 'old_link', 'date', 'title', 'excerpt', 'parent')
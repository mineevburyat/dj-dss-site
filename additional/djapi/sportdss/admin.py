from django.contrib import admin
from .models import BaseCategory, Service, Object, Managment
from .models import About, Phone, Email, Contact, WorkingMode
# admin.site.register(BaseCategory)
# admin.site.register(Service)
# admin.site.register(Object)
# 
@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('short_name', 'name', 'address', 'category', 'display_service', 'display_sportsection')


@admin.register(BaseCategory)
class BaseCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'title', 'newname')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'descriprion', 'category')

@admin.register(Managment)
class ManagmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job_title', 'object', 'photo', 'contact', 'about')

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'object', 'display_phones', 'display_email', 'about')

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('phone', 'contact')

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'contact')

@admin.register(WorkingMode)
class WorkingModeAdmin(admin.ModelAdmin):
    list_display = ('contact', 'display_mode')
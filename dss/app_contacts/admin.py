from django.contrib import admin
from .models import Contact, Phone

# Register your models here.

class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 0

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'email', 'get_phones_str')
    ordering = ('sportarea',)
    inlines = [PhoneInline]
    
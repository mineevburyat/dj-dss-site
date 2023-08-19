from django.contrib import admin
from .models import Contact, Phone

# Register your models here.

class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 0

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'get_phones_str', 'get_object_str',)
    ordering = ('obj',)
    inlines = [PhoneInline]
    
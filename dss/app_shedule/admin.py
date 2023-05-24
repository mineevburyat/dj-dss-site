from django.contrib import admin
from .models import Shedule
# Register your models here.


@admin.register(Shedule)
class SheduleAdmin(admin.ModelAdmin):
    pass
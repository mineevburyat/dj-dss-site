from django.contrib import admin
from .models import Shedule
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

# Register your models here.


@admin.register(Shedule)
class SheduleAdmin(admin.ModelAdmin):
    formfield_overrides = {
        # fields.JSONField: {'widget': JSONEditorWidget}, # if django < 3.1
        models.JSONField: {'widget': JSONEditorWidget},
    }
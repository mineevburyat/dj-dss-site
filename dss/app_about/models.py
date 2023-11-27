from django.db import models
from app_objects.models import Object
from app_mediafiles.models import Image
# Create your models here.

class Manager(models.Model):
    '''\
        Руководители объектов и руководитель руководителей'''
    class Meta:
        verbose_name = 'руководитель'
        verbose_name_plural = 'руководители'

    job_title = models.CharField(
        'должность',
        max_length=200,
        help_text='поное название'
    )
    full_name = models.CharField(
        'полное имя',
        unique=True,
        db_index=True,
        max_length=250,
    )
    photo = models.OneToOneField(
        Image,
        verbose_name='фотография',
        on_delete=models.PROTECT
    )
    
    
    def __str__(self):
        return f"{self.full_name}"
    
    
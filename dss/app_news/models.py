from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from pathlib import Path
from django.conf import settings
from PIL import Image as PImage
from django.core.files import File
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.files.base import ContentFile
from io import BytesIO
import os
from app_mediafiles.models import Image
# Create your models here.

        
class News(models.Model):
    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        
    slug = models.SlugField(
        max_length=100,
        db_index=True,
    )
    date_public = models.DateTimeField(
        'дата публикации',
    )
    title = models.CharField(
        'заголовок',
        max_length=100,
    )
    excerpt = models.TextField(
        'отрывок',
        max_length=250,
        blank=True,
        null=True
    )
    content = models.TextField(
        'содержание',
        max_length=2000,
    )
    featured_media = models.ForeignKey(
        Image,
        verbose_name='id media',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    
    def get_thumbnail(self):
        if self.featured_media:
            return mark_safe(f'<a href="{self.featured_media.large.url}"><img src="{self.featured_media.thumbnail.url}" alt="{self.featured_media.alt_txt}"></a>')
    

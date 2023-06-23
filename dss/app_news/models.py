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
from app_tags.models import Tag
from datetime import datetime
# Create your models here.


MAX_TITLE = 110
MAX_EXCERPT = 550
MAX_CONTENT = 2500


class News(models.Model):
    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        
    slug = models.SlugField(
        max_length=MAX_TITLE,
        db_index=True,
        unique=True
    )
    date_public = models.DateTimeField(
        'дата публикации',
        auto_now_add=True
    )
    title = models.CharField(
        'заголовок',
        max_length=MAX_TITLE,
    )
    excerpt = models.TextField(
        'отрывок',
        max_length=MAX_EXCERPT,
        blank=True,
        null=True
    )
    content = models.TextField(
        'содержание',
        max_length=MAX_CONTENT,
    )
    featured_media = models.ForeignKey(
        Image,
        verbose_name='id media',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        # related_name='tags'
        )
    important = models.BooleanField(
        'на первую полосу',
        default=False
    )
    valid_until_date = models.DateTimeField(
        'действует до',
        blank=True,
        null=True
    )
    date_activation = models.DateTimeField(
        'дата активации',
        default=datetime.now,
    )
    
    def get_thumbnail(self):
        if self.featured_media:
            return mark_safe(f'<a href="{self.featured_media.large.url}"><img src="{self.featured_media.thumbnail.url}" alt="{self.featured_media.alt_txt}"></a>')
    
    def tags_list(self):
        lst = [x[1] for x in self.tags.values_list()]
        return mark_safe('<br>'.join(lst))
    tags.short_description = 'тэги'
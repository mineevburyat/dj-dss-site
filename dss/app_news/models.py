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
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


MAX_TITLE = 210
MAX_EXCERPT = 550
MAX_CONTENT = 3500


class News(models.Model):
    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        
    slug = models.SlugField(
        max_length=MAX_TITLE,
        db_index=True,
        unique=True
    )
    compose_date = models.DateTimeField(
        'дата добавления',
        auto_now_add=timezone.now)
    date_public = models.DateTimeField(
        'дата публикации',
        default=datetime.now,
    )
    date_activation = models.DateTimeField(
        'дата активации',
        default=datetime.now,
    )
    valid_until_date = models.DateTimeField(
        'действует до',
        blank=True,
        null=True
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
    content = RichTextUploadingField(
        'содержание',
        max_length=MAX_CONTENT,
    )
    featured_media = models.ForeignKey(
        Image,
        verbose_name='id media',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='news'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        # related_name='tags'
        )
    important = models.BooleanField(
        'важная',
        default=False
    )
    level_importance = models.CharField(
        max_length=8,
        choices=[
            ('danger', 'важный'),
            ('warning', 'предупреждение'),
            ('info', 'информация'),],
        default='info')
    
    
    def get_thumbnail(self):
        if self.featured_media:
            return mark_safe(f'<a href="{self.featured_media.large.url}"><img src="{self.featured_media.thumbnail.url}" alt="{self.featured_media.alt_txt}"></a>')
    
    def tags_list(self):
        lst = [x[1] for x in self.tags.values_list()]
        return mark_safe('<br>'.join(lst))
    tags.short_description = 'тэги'
    
    def __str__(self):
        start_date = self.date_activation.strftime('%d.%m.%Y %H:%M')
        end_date = self.valid_until_date.strftime('%d.%m.%Y %H:%M')
        return f"{self.title} ({start_date} - {end_date})"
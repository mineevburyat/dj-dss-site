from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from app_mediafiles.models import Image


# Create your models here.
class Piple(models.Model):
    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'
        
    fullname = models.CharField(
        'полное имя',
        max_length=120
    )
    description = RichTextUploadingField(
        'краткое описание',
        max_length=650
    )
    photo = models.ForeignKey(
        Image,
        verbose_name='фото',
        on_delete=models.PROTECT
    )
    
    def get_thumbnail_html(self):
        return self.photo.thumbnail_html()
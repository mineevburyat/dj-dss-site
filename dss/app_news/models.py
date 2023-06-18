from django.db import models
from django.urls import reverse
from .templatetags.fsize_tag import filesize
from django.utils.safestring import mark_safe
from pathlib import Path
from django.conf import settings
from PIL import Image as PImage
from django.core.files import File
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.core.files.base import ContentFile
from io import BytesIO
from .templatetags.fsize_tag import filesize
import os

# Create your models here.

class ImageMedia(models.Model):
    class Meta:
        verbose_name = 'Изобажение'
        verbose_name_plural = 'Галерея'
    slug = models.SlugField(
        'часть url',
        max_length=120,
        db_index=True,
        unique=True
        )
    title = models.CharField(
        'название',
        db_index=True,
        max_length=120)
    caption = models.TextField(
        'подпись к картинке',
        db_index=True,
        max_length=500
        )
    alt_txt = models.CharField(
        'альтернативная подпись',
        max_length=160
        )
    date_public = models.DateTimeField(
        'время добавления',
        auto_now_add=True
        )
    img_file_size = models.IntegerField(
        'объем файла',
        blank=True,
        null=True
        )
    img_mode = models.CharField(
        max_length=10,
        help_text='color, grey, and other',
        blank=True,
        null=True
        )
    width = models.IntegerField(
        'ширина в пикселях',
        blank=True,
        null=True
    )
    height = models.IntegerField(
        'высота в пикселях',
        blank=True,
        null=True
    )
    image = models.ImageField(
        'картинка',
        upload_to="media_image")
    media_type = models.CharField(
        'расширение',
        max_length=5,
        help_text='расширение файла',
        blank=True,
        null=True)
    thumbnail = models.ImageField(
        'width 150',
        blank=True,
        null=True,
        upload_to='media_image/thumbnail'
    )
    medium = models.ImageField(
        'with 320',
        blank=True,
        null=True,
        upload_to='media_image/medium'
    )
    large = models.ImageField(
        'with 1080',
        blank=True,
        null=True,
        upload_to='media_image/large'
    )
        
    def __str__(self):
        return f"{self.title} ({self.pk})"
    
    def is_caption(self):
        return bool(self.caption)
    is_caption.boolean = True
    is_caption.short_description = 'Имеется подпись картинки'
    
    def get_img_size(self):
        return f"{self.width}x{self.height}"
    get_img_size.short_description = 'размер картинки'
    
    def get_absolute_url(self):
        return reverse("app_news:detailimg", kwargs={"slug": self.slug})
    
    def get_next_slug(self):
        next = ImageMedia.objects.filter(pk__gt = self.pk).order_by('pk').first()
        if next:
            return next.slug
    
    def get_prev_slug(self):
        prev = ImageMedia.objects.filter(pk__lt = self.pk).order_by('-pk').first()
        if prev:
            return prev.slug
        
    def get_fsize(self):
        return filesize(self.img_file_size)
    get_fsize.short_description = 'размер файла'
    
    def get_large_html(self):
        img = PImage.open(self.large)
        width, height = img.size
        name = self.large.name
        fimg = BytesIO()
        img.save(fimg, img.format)
        fsize = filesize(len(fimg.getvalue()))
        return mark_safe(f"<a href={self.large.url}>{name} ({width}x{height}) {fsize}</a>")
        
    def get_medium_html(self):
        img = PImage.open(self.medium)
        width, height = img.size
        name = self.medium.name
        fimg = BytesIO()
        img.save(fimg, img.format)
        fsize = filesize(len(fimg.getvalue()))
        return mark_safe(f"<a href={self.medium.url}>{name} ({width}x{height}) {fsize}</a>")
    
    def get_small_html(self):
        img = PImage.open(self.thumbnail)
        width, height = img.size
        name = self.thumbnail.name
        fimg = BytesIO()
        img.save(fimg, img.format)
        fsize = filesize(len(fimg.getvalue()))
        return mark_safe(f"<a href={self.thumbnail.url}>{name} ({width}x{height})  {fsize}</a>")


        
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
        ImageMedia,
        verbose_name='id media',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    
    def get_thumbnail(self):
        if self.featured_media:
            return mark_safe(f'<a href="{self.featured_media.large.url}"><img src="{self.featured_media.thumbnail.url}" alt="{self.featured_media.alt_txt}"></a>')
    
@receiver(post_save, sender=ImageMedia)
def fill_field_image(sender, instance, created, **kwargs):
    '''после сохранения экземпляра с оригинальной фотографией, узнать его размеры и сгенерировать миниатюры с различными размерами'''
    THUMBNAIL = 150
    MEDIUM = 320
    LARGE = 1080
    miniature = {
        'large': LARGE,
        'medium': MEDIUM,
        'thumbnail': THUMBNAIL
    }
    if created:
        img = PImage.open(instance.image)
        if not instance.width:
            instance.width, instance.height = img.size
        instance.img_mode = img.mode
        img_format = img.format
        if not instance.media_type:
            instance.media_type = img_format
        if not instance.img_file_size:
            instance.img_file_size = Path(instance.image.path).stat().st_size
        # instance.save()
        # имя и расширение
        exten = Path(instance.image.name).suffix[1:]
        fname = Path(instance.image.name).stem
        # сгенерировать миниатюры
        for field, im_size in miniature.items():
            inst_attr = getattr(instance, field)
            if not inst_attr.name:
                if instance.width > im_size:
                    percent = im_size / float(instance.width)
                    new_hight = int(instance.height * percent)
                    img_resize = img.resize((im_size, new_hight))
                else:
                    img_resize = img.copy()
                newfilename = f"{field[0]}_{fname}.{exten}"
                file_bufer = BytesIO()
                img_resize.save(file_bufer, img_format)
                file_bufer.seek(0)
                inst_attr.save(
                        newfilename,
                        ContentFile(file_bufer.read()),
                        save=True)
                file_bufer.close()
                inst_attr.close()
                print(field, 'success')
        instance.save()
        img.close()
        
@receiver(post_delete, sender=ImageMedia)
def del_field_image(sender, instance,  **kwargs):
    '''после удаления экземпляра с оригинальной фотографией, удалить связанный файл и его миниатюры'''
    os.remove(instance.image.path)
    os.remove(instance.large.path)
    os.remove(instance.medium.path)
    os.remove(instance.thumbnail.path)
    
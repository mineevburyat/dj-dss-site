from django.db import models
import uuid
from pathlib import Path
from django.conf import settings
from django.utils.safestring import mark_safe
from PIL import Image as PImage
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from io import BytesIO



IMAGE_FOLDER_ICON = 'imagelibrary/icon'
IMAGE_FOLDER_PHOTO = 'imagelibrary/photo'
THUB_MIDDLE = 'thumbnail_middle'
THUB_SMALL = 'thumbnail_small'

def path_icon_file(instance, filename):
    extentions = Path(filename).suffix[1:]
    filename = f"{uuid.uuid4()}.{extentions}"
    path = Path(IMAGE_FOLDER_ICON, filename)
    return path

def path_photo_file(instance, filename):
    extentions = Path(filename).suffix[1:]
    filename = f"{uuid.uuid4()}.{extentions}"
    path = Path(IMAGE_FOLDER_PHOTO, filename)
    return path

class Icon(models.Model):
    """
    Иконка и связанная с иконкой текстовая информация
    """
    class Meta:
        verbose_name = 'Иконка'
        verbose_name_plural = 'Иконки'
    name = models.CharField(max_length=60,
                            default='иконка ...',
                            help_text='иконка бассейна, иконка стадиона и пр.')
    image = models.ImageField(
        upload_to=path_icon_file,
    )
    created = models.DateTimeField('дата создания', auto_now_add=True)
    width = models.IntegerField('ширина', blank=True, null=True)
    height = models.IntegerField('высота', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        """После сохранения получить размеры иконки. Так не надо делать.
        Альтернатива - сигналы pre_save и post_save"""
        super(Icon, self).save(*args, **kwargs)
        # image = PImage.open(car.photo)
        im = PImage.open(Path(settings.MEDIA_ROOT, self.image.name))
        self.width, self.height = im.size
        super(Icon,self).save(*args, **kwargs)
    
    def get_icon_url(self):
        if not self.image:
            return '/media/emptyicon.png'
        return self.image.url
    
    def icon_html_img(self):
        return mark_safe(f'<img src="{self.get_icon_url()}" alt="{self.name}" style="width:80px">')
    icon_html_img.short_description = 'Иконка'
    
    def __str__(self):
        return f'{self.name} (иконка)'
    
    def img_size(self):
        """Image size."""
        return "%s x %s" % (self.width, self.height)
    img_size.short_description = 'размер'
    
    
class Tag(models.Model):
    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
    tag = models.CharField(max_length=50)
    def __str__(self):
        return self.tag
    
class Image(models.Model):
    '''\
        Медиабиблиотека изображений, где каждый элемент имеет описание, имя, размер оригинала и миниатюры'''
    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'
    name = models.CharField('название (alt)', max_length=60)
    description = models.TextField('описание', max_length=260)
    image = models.ImageField('файл картинки', upload_to=path_photo_file)
    tags = models.ManyToManyField(Tag, blank=True)
    created = models.DateTimeField('дата создания', auto_now_add=True)
    width = models.IntegerField('ширина', blank=True, null=True)
    height = models.IntegerField('высота', blank=True, null=True)
    thumbnail_middle = models.ImageField(
        'средняя миниатюра',
        upload_to=Path(IMAGE_FOLDER_PHOTO, THUB_MIDDLE),
        blank=True,
        null=True)
    thumbnail_small = models.ImageField(
        'миниминиатюра',
        upload_to=Path(IMAGE_FOLDER_PHOTO, THUB_SMALL),
        blank=True,
        null=True)
    
    def get_path_forigin(self):
        return self.image.name
    
    def get_path_fmedium(self):
        return self.thumbnail_middle.name
    
    def get_path_fsmall(self):
        return self.thumbnail_small.name
    
    def get_img_url(self):
        if not self.image:
            return '/media/emptyhumbnail.png'
        return self.image.url
    
    def photo_img(self):
        return mark_safe(
            f'<img src="{self.get_img_url()}" alt="{self.name}" style="width:50%;">')
    photo_img.short_description = 'Картинка'
    
    def thumbnail_html(self):
        return mark_safe(f'<a href="{self.image.url}"><img border="0" alt="" src="{self.thumbnail_small.url}" height="50" /></a>')
    thumbnail_html.allow_tags = True
    thumbnail_html.short_description = 'изображение'
    
    def __str__(self):
        return self.name
    
    def img_size(self):
        """Image size."""
        return "%s x %s" % (self.width, self.height)
    img_size.short_description = 'размер'

    def tags_(self):
        lst = [x[1] for x in self.tags.values_list()]
        return ','.join(lst)
    tags.short_description = 'тэги'
    
    


@receiver(post_save, sender=Image)
def fill_field_image(sender, instance, created, **kwargs):
    '''после сохранения экземпляра с оригинальной фотографией, узнать его размеры и сгенерировать миниатюры из него'''
    if created:
        im = PImage.open(Path(settings.MEDIA_ROOT, instance.image.name))
        instance.width, instance.height = im.size
        format = im.format
        instance.save()
        # имя и расширение
        extention = Path(instance.image.name).suffix[1:]
        fname = Path(instance.image.name).stem
        # миниатюра среднего размера
        thbnail_medium = im.resize((instance.width // 4, instance.height // 4))
        newfilename = f"m_{fname}.{extention}"
        file_bufer = BytesIO()
        thbnail_medium.save(file_bufer, format)
        file_bufer.seek(0)
        instance.thumbnail_middle.save(
                newfilename,
                ContentFile(file_bufer.read()),
                save=False)
        file_bufer.close()
        # миниатюра самая маленькая
        newfilename = f"s_{fname}.{extention}"
        thumbnail_small = thbnail_medium.resize((instance.width // 8, instance.height // 8))
        file_bufer = BytesIO()
        thumbnail_small.save(file_bufer, format)
        file_bufer.seek(0)
        instance.thumbnail_small.save(
            newfilename,
                ContentFile(file_bufer.read()),
                save=False)
        file_bufer.close()
        instance.save()
        
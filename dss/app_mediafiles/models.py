from django.db import models
import uuid
from pathlib import Path
from django.conf import settings
from django.utils.safestring import mark_safe
from PIL import Image as PImage
from django.core.files import File

IMAGE_FOLDER_ICON = 'imagelibrary/icon'
IMAGE_FOLDER_PHOTO = 'imagelibrary/photo'

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
    name = models.CharField(max_length=60, default='иконка ...')
    image = models.ImageField(
        upload_to=path_icon_file,
    )
    
    def get_icon_url(self):
        if not self.image:
            return '/media/emptyicon.png'
        return self.image.url
    
    def icon_html_card(self):
        return mark_safe(
            f'''<div style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                transition: 0.3s; width: 150px; margin: 10px">
                    <img src="{self.get_icon_url()}" alt="{self.name}" style="width:100%">
                    <div style="padding: 2px 16px;">
                        <h4><b>{self.name}</b></h4>
                    </div>
                </div>''')
    icon_html_card.short_description = 'Иконка'
    
    def __str__(self):
        return f'{self.name}'
    
    
class Tag(models.Model):
    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
    tag = models.CharField(max_length=50)
    def __str__(self):
        return self.tag
    
class Image(models.Model):
    '''\
        Изображение с описанием, именем и миниатюрами'''
    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'
    name = models.CharField('название (alt)', max_length=60)
    description = models.CharField('описание', max_length=260)
    image = models.ImageField(upload_to=path_photo_file)
    tags = models.ManyToManyField(Tag, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    thumbnail_middle = models.ImageField(
        upload_to=f"{IMAGE_FOLDER_PHOTO}/thumbnail_middle",
        blank=True,
        null=True)
    thumbnail_small = models.ImageField(
        upload_to=f"{IMAGE_FOLDER_PHOTO}/thumbnail_small",
        blank=True,
        null=True)
    
    def get_img_url(self):
        if not self.image:
            return '/media/emptyicon.png'
        return self.image.url
    
    def photo_html_img(self):
        return mark_safe(
            f'<img src="{self.get_icon_url()}" alt="{self.name}" style="width:25%">')
    photo_html_img.short_description = 'Картинка'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Save image dimensions."""
        super(Image, self).save(*args, **kwargs)
        # image = PImage.open(car.photo)
        im = PImage.open(Path(settings.MEDIA_ROOT, self.image.name))
        self.width, self.height = im.size
        extention = Path(self.image.name).suffix
        fname = Path(self.image.name).stem
        thbnail_medium = im.copy()
        thbnail_medium.thumbnail((self.width // 4, self.height // 4),
                                 PImage.ANTIALIAS)
        newfilename = f"thumbnail_medium_{fname}.{extention}"
        path = Path(settings.MEDIA_ROOT, newfilename)
        thbnail_medium.save(path)
        with open(path, 'br') as f:
            self.thumbnail_middle.save(newfilename, File(f), save=False)
            
        thbnail_small = thbnail_medium.copy()
        thbnail_small.thumbnail((self.width // 8, self.height //8),
                                PImage.ANTIALIAS)
        newfilename = f"thumbnail_small_{fname}.{extention}"
        path = Path(settings.MEDIA_ROOT, newfilename)
        thbnail_small.save(path)
        with open(path, 'br') as f:
            self.thumbnail_small.save(newfilename, File(f), save=False)
        super(Image, self).save(*args, **kwargs)

    def img_size(self):
        """Image size."""
        return "%s x %s" % (self.width, self.height)

    def tags_(self):
        lst = [x[1] for x in self.tags.values_list()]
        return ','.join(lst)

    def get_thumbnail_html(self):
        return mark_safe(f'<a href="{self.image.url}"><img border="0" alt="" src="{self.image.url}" height="40" /></a>')
    get_thumbnail_html.allow_tags = True


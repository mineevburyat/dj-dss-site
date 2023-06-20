from django.db import models
import uuid
from pathlib import Path
from django.conf import settings
from django.utils.safestring import mark_safe
from PIL import Image as PImage
from django.core.files import File
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.files.base import ContentFile
from io import BytesIO
from django.urls import reverse
from .templatetags.fsize_tag import filesize
from django.utils.safestring import mark_safe
import os

# папки для иконок и фотографий
IMAGE_FOLDER_ICON = 'imagelibrary/icon'
IMAGE_FOLDER_PHOTO = 'imagelibrary/photo'
# подпапки миниатюр
MIDDLE = 'middle'
SMALL = 'thumbnail'
LARGE = 'large'
# размеры миниатюр
WIDTH_THUMBNAIL = 150
WIDTH_MEDIUM = 320
WIDTH_LARGE = 1080
# максимальная длинна файла
MAX_LEN_FILENAME = 70
# поля для миниатюр в экземпляре фотографии
MAX_TITLE = 90
MAX_CAPTION = 260
miniature = {
        'large': WIDTH_LARGE,
        'medium': WIDTH_MEDIUM,
        'thumbnail': WIDTH_THUMBNAIL
    }


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

def filename_photo_file(instance, filename):
    extentions = Path(filename).suffix[1:]
    filename = Path(filename).stem
    if len(filename) > MAX_LEN_FILENAME:
        filename = filename[:MAX_LEN_FILENAME]
    path = Path(IMAGE_FOLDER_PHOTO, f"{filename}.{extentions}")
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
    image = models.ImageField(upload_to=path_icon_file)
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
    
    
# class ImageMedia(models.Model):
#     class Meta:
#         verbose_name = 'Изобажение'
#         verbose_name_plural = 'Галерея изображений'
        
#     slug = models.SlugField(
#         'часть url',
#         max_length=120,
#         db_index=True,
#         unique=True)
#     title = models.CharField(
#         'название',
#         db_index=True,
#         max_length=120)
#     caption = models.TextField(
#         'подпись к картинке',
#         db_index=True,
#         max_length=500)
#     alt_txt = models.CharField(
#         'альтернативная подпись',
#         max_length=160)
#     date_public = models.DateTimeField(
#         'время добавления',
#         auto_now_add=True)
#     img_file_size = models.IntegerField(
#         'объем файла',
#         blank=True,
#         null=True)
#     img_mode = models.CharField(
#         max_length=10,
#         help_text='color, grey, and other',
#         blank=True,
#         null=True)
#     width = models.IntegerField(
#         'ширина в пикселях',
#         blank=True,
#         null=True)
#     height = models.IntegerField(
#         'высота в пикселях',
#         blank=True,
#         null=True)
#     media_type = models.CharField(
#         'расширение',
#         max_length=5,
#         help_text='расширение файла',
#         blank=True,
#         null=True)
#     image = models.ImageField(
#         'оригинал',
#         upload_to=filename_photo_file)
#     thumbnail = models.ImageField(
#         'миниатюра самая маленькая',
#         blank=True,
#         null=True,
#         upload_to=Path(IMAGE_FOLDER_PHOTO, SMALL),)
#     medium = models.ImageField(
#         'миниатюра средняя',
#         blank=True,
#         null=True,
#         upload_to=Path(IMAGE_FOLDER_PHOTO, MIDDLE))
#     large = models.ImageField(
#         'миниатюра большая',
#         blank=True,
#         null=True,
#         upload_to=Path(IMAGE_FOLDER_PHOTO, LARGE))
#     tags = models.ManyToManyField(Tag, blank=True)
        
#     def __str__(self):
#         return f"{self.title} ({self.pk})"
    
#     def is_caption(self):
#         return bool(self.caption)
#     is_caption.boolean = True
#     is_caption.short_description = 'Имеется подпись картинки'
    
#     def get_img_size(self):
#         return f"{self.width}x{self.height}"
#     get_img_size.short_description = 'размер картинки'
    
#     def get_absolute_url(self):
#         return reverse("app_news:detailimg", kwargs={"slug": self.slug})
    
#     def get_next_slug(self):
#         next = ImageMedia.objects.filter(pk__gt = self.pk).order_by('pk').first()
#         if next:
#             return next.slug
    
#     def get_prev_slug(self):
#         prev = ImageMedia.objects.filter(pk__lt = self.pk).order_by('-pk').first()
#         if prev:
#             return prev.slug
        
#     def get_fsize(self):
#         return filesize(self.img_file_size)
#     get_fsize.short_description = 'размер файла'
    
#     def get_large_html(self):
#         img = PImage.open(self.large)
#         width, height = img.size
#         name = self.large.name
#         fimg = BytesIO()
#         img.save(fimg, img.format)
#         fsize = filesize(len(fimg.getvalue()))
#         return mark_safe(f"<a href={self.large.url}>{name} ({width}x{height}) {fsize}</a>")
        
#     def get_medium_html(self):
#         img = PImage.open(self.medium)
#         width, height = img.size
#         name = self.medium.name
#         fimg = BytesIO()
#         img.save(fimg, img.format)
#         fsize = filesize(len(fimg.getvalue()))
#         return mark_safe(f"<a href={self.medium.url}>{name} ({width}x{height}) {fsize}</a>")
    
#     def get_small_html(self):
#         img = PImage.open(self.thumbnail)
#         width, height = img.size
#         name = self.thumbnail.name
#         fimg = BytesIO()
#         img.save(fimg, img.format)
#         fsize = filesize(len(fimg.getvalue()))
#         return mark_safe(f"<a href={self.thumbnail.url}>{name} ({width}x{height})  {fsize}</a>")
    
    # def get_path_forigin(self):
    #     return self.image.name
    
    # def get_path_fmedium(self):
    #     if self.medium:
    #         return self.medium.name
    
    # def get_path_fsmall(self):
    #     if self.thumbnail:
    #         return self.thumbnail.name
        
    # def get_url_middle_img(self):
    #     if self.thumbnail_small:
    #         return self.image.url
    
    # def get_img_url(self):
    #     if not self.image:
    #         return '/media/emptyhumbnail.png'
    #     return self.image.url
    
    # def photo_img(self):
    #     return mark_safe(
    #         f'<img src="{self.get_img_url()}" alt="{self.alt_txt}" style="width:50%;">')
    # photo_img.short_description = 'Картинка'
    
    # def thumbnail_html(self):
    #     if self.thumbnail:
    #         return mark_safe(f'<a href="{self.image.url}"><img border="0" alt="" src="{self.thumbnail_small.url}" height="50" /></a>')
    #     elif self.thumbnail_middle:
    #         return mark_safe(f'<a href="{self.image.url}"><img border="0" alt="" src="{self.thumbnail_middle.url}" height="50" /></a>')
    #     else:
    #         return mark_safe(f'<a href="{self.image.url}"><img border="0" alt="" src="{self.image.url}" height="50" /></a>')
    # thumbnail_html.allow_tags = True
    # thumbnail_html.short_description = 'изображение'

class Image(models.Model):
    '''\
        Медиабиблиотека изображений, где каждый элемент имеет описание, имя, размер оригинала и миниатюры'''
    class Meta:
        verbose_name = 'Изобажение'
        verbose_name_plural = 'Галерея изображений'
    title = models.CharField('заголовок', max_length=MAX_TITLE)
    caption = models.TextField('подпись-описание', max_length=MAX_CAPTION)
    slug = models.SlugField(
        'часть url',
        max_length=MAX_TITLE,
        db_index=True,
        unique=True
        )
    alt_txt = models.CharField(
        'альтернативная подпись',
        max_length=MAX_TITLE,
        default='fill necessarily! ')
    date_public = models.DateTimeField('дата создания', auto_now_add=True)
    img_file_size = models.IntegerField(
        'объем файла',
        blank=True,
        null=True)
    img_mode = models.CharField(
        max_length=10,
        blank=True,
        null=True)
    width = models.IntegerField('ширина', blank=True, null=True)
    height = models.IntegerField('высота', blank=True, null=True)
    media_type = models.CharField(
        'расширение',
        max_length=5,
        help_text='расширение файла',
        blank=True,
        null=True)
    image = models.ImageField('файл картинки', upload_to=path_photo_file)
    thumbnail = models.ImageField(
        'миниатюра самая маленькая',
        blank=True,
        null=True,
        upload_to=Path(IMAGE_FOLDER_PHOTO, SMALL),)
    medium = models.ImageField(
        'миниатюра средняя',
        blank=True,
        null=True,
        upload_to=Path(IMAGE_FOLDER_PHOTO, MIDDLE))
    large = models.ImageField(
        'миниатюра большая',
        blank=True,
        null=True,
        upload_to=Path(IMAGE_FOLDER_PHOTO, LARGE))
    tags = models.ManyToManyField(Tag, blank=True)
    
    
    # def get_path_forigin(self):
    #     return self.image.name
    
    # def get_path_fmedium(self):
    #     if self.medium:
    #         return self.medium.name
    
    # def get_path_fsmall(self):
    #     if self.thumbnail:
    #         return self.thumbnail.name
        
    # def get_url_middle_img(self):
    #     if self.thumbnail:
    #         return self.image.url
    
    def photo_img(self, max_width=400):
        if not self.image:
            return '/media/emptyhumbnail.png'
        if max_width < WIDTH_THUMBNAIL:
            return mark_safe(f'<a href="{self.image.url}"><img border="0" alt="" src="{self.thumbnail.url}" width="{max_width}" /></a>')
        elif WIDTH_THUMBNAIL <= max_width < WIDTH_MEDIUM:
            return mark_safe(f'<a href="{self.image.url}"><img border="0" alt="" src="{self.medium.url}" width="{max_width}" /></a>')
        else:
            return mark_safe(f'<a href="{self.image.url}"><img border="0" alt="" src="{self.large.url}" width="{max_width}" /></a>')
    photo_img.short_description = ''
        
    def thumbnail_html(self):
        if self.thumbnail:
            return mark_safe(f'<a href="{self.image.url}"><img border="0" alt="" src="{self.thumbnail.url}" height="50" /></a>')
        elif self.medium:
            return mark_safe(f'<a href="{self.image.url}"><img border="0" alt="" src="{self.medium.url}" height="50" /></a>')
        else:
            return mark_safe(f'<a href="{self.image.url}"><img border="0" alt="" src="{self.image.url}" height="50" /></a>')
    thumbnail_html.allow_tags = True
    thumbnail_html.short_description = 'миниатюра'
    
    def __str__(self):
        return f"{self.title} ({self.pk})"
    
    def get_img_size(self):
        return f"{self.width}x{self.height} px"
    get_img_size.short_description = 'размер картинки'

    def tags_list(self):
        lst = [x[1] for x in self.tags.values_list()]
        return mark_safe('<br>'.join(lst))
    tags.short_description = 'тэги'
    
    def is_caption(self):
        return bool(self.caption)
    is_caption.boolean = True
    is_caption.short_description = 'есть подпись'
    
    def get_absolute_url(self):
        return reverse("app_news:detailimg", kwargs={"slug": self.slug})
    
    def get_next_slug(self):
        next = Image.objects.filter(pk__gt = self.pk).order_by('pk').first()
        if next:
            return next.slug
    
    def get_prev_slug(self):
        prev = Image.objects.filter(pk__lt = self.pk).order_by('-pk').first()
        if prev:
            return prev.slug
        
    def get_fsize(self):
        return filesize(self.img_file_size)
    get_fsize.short_description = 'размер файла'
    
    def get_large_html(self):
        if os.path.exists(self.large.path):
            img = PImage.open(self.large)
            width, height = img.size
            name = self.large.name
            fimg = BytesIO()
            img.save(fimg, img.format)
            fsize = filesize(len(fimg.getvalue()))
            return mark_safe(f"<a href={self.large.url}>{name} ({width}x{height}) {fsize}</a>")
        
    def get_medium_html(self):
        if os.path.exists(self.medium.path):
            img = PImage.open(self.medium)
            width, height = img.size
            name = self.medium.name
            fimg = BytesIO()
            img.save(fimg, img.format)
            fsize = filesize(len(fimg.getvalue()))
            return mark_safe(f"<a href={self.medium.url}>{name} ({width}x{height}) {fsize}</a>")
    
    def get_small_html(self):
        if os.path.exists(self.thumbnail.path):
            img = PImage.open(self.thumbnail)
            width, height = img.size
            name = self.thumbnail.name
            fimg = BytesIO()
            img.save(fimg, img.format)
            fsize = filesize(len(fimg.getvalue()))
            return mark_safe(f"<a href={self.thumbnail.url}>{name} ({width}x{height})  {fsize}</a>")



        
@receiver(post_save, sender=Image)
def fill_field_image(sender, instance, created, **kwargs):
    '''после сохранения экземпляра с оригинальной фотографией, узнать его размеры и сгенерировать миниатюры с различными размерами'''
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
        
@receiver(post_delete, sender=Image)
def del_field_image(sender, instance,  **kwargs):
    '''после удаления экземпляра с оригинальной фотографией, удалить связанный файл и его миниатюры'''
    if instance.medium.name != '' and os.path.exists(instance.image.path):
        os.remove(instance.image.path)
    if instance.large.name != '' and os.path.exists(instance.large.path):
        os.remove(instance.large.path)
    if instance.medium.name != '' and os.path.exists(instance.medium.path):
        os.remove(instance.medium.path)
    if instance.thumbnail.name != '' and os.path.exists(instance.thumbnail.path):
        os.remove(instance.thumbnail.path)
    
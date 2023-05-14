from django.db import models
from django.urls import reverse
from common.utils import translite
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField


class Service(models.Model):
    '''\
        Услуги согласно категории:
        спортивная, секция, прочая '''
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    MAX_NAME_LENGTH = 60

    CHOICE_CATEGORY = (
        ('sport', 'Спортивные услуги'),
        ('section', 'Спортивные секции'),
        ('other', 'Прочие услуги')
    )
    MAX_PREF_LENGTH = 10

    name = models.CharField(
        'название услуги',
        max_length=MAX_NAME_LENGTH
    )
    description = RichTextUploadingField(
        'краткое описание',
        max_length=1000
    )
    category = models.CharField(
        'категория услуги',
        choices=CHOICE_CATEGORY,
        max_length=MAX_PREF_LENGTH,
    )
    slug = models.SlugField(
        'slug имя в url',
        unique=True,
        db_index=True,
        max_length=MAX_NAME_LENGTH,
        blank=True,
        null=True,
        help_text='только латинские буквы и цифры'
    )
    icon = models.ImageField(
        'файл иконки',
        upload_to='services',
        blank=True,
        null=True
    )
    photo = models.ImageField(
        'файл фотографии',
        help_text='в будущем набор фотографий для слайдера',
        upload_to='services',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f"{self.name}"

    # def save(self, *args, **kwargs):
    #     self.slug = translite(self.name)
    #     super(self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('services:detail', kwargs={"slug": self.slug})
    
    def get_icon_url(self):
        if not self.icon:
            return '/media/emptyicon.png'
        return self.icon.url
    
    def icon_html_img(self):
        return mark_safe(
            f'<img src="{self.get_icon_url()}" width="50" height="50" />')
    icon_html_img.short_description = 'Иконка'
    
    def get_photo_url(self):
        if not self.photo:
            return '/media/emptyphoto.jpg'
        return self.photo.url
    
    def photo_html_img(self):
        return mark_safe(
            f'<img src="{self.get_photo_url()}" width="150"/>')
    photo_html_img.short_description = 'Фото'
    # def display_objects(self):
    #     lst = [item.short_name for item in Object.objects.filter(service = self.id) ]
    #     return ' '.join(lst)
    
class VariousSport(models.Model):
    class Meta:
        verbose_name = 'Вид спорта'
        verbose_name_plural = 'Виды спорта'
    name = models.CharField(
        'Название спорта',
        max_length=60
    )
    slug = models.CharField(
        'название на английском',
        max_length=60
    )
    
    def __str__(self):
        return f"{self.name} ({self.slug})"
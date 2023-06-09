from django.db import models
from django.urls import reverse
from common.utils import translite
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from app_mediafiles.models import Icon, Image

# искуственные категории услуг
MAX_PREF_LENGTH = 10
CHOICE_CATEGORY = (
        ('sport', 'Спортивные услуги'),
        ('section', 'Спортивные секции'),
        ('relax', 'Отдых'),
        ('other', 'Прочие услуги'),
    )

class VariousSport(models.Model):
    '''\
        вид спорта: по общероссийской классификации'''
    class Meta:
        verbose_name = 'Вид спорта'
        verbose_name_plural = 'Виды спорта'
    name = models.CharField(
        'Название спорта',
        max_length=60,
        unique=True
    )
    slug = models.CharField(
        'название на английском',
        max_length=60,
        unique=True,
        db_index=True
    )
    
    def __str__(self):
        return f"{self.name} ({self.slug})"
    
class TypeService(models.Model):
    '''\
        Группировка услуг на исскуственные типы для меню'''
    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'
        
    name = models.CharField(
        'Название группы услуг',
        max_length=60,
        unique=True,
        db_index=True
    )
    slug = models.CharField(
        'название на английском',
        max_length=60,
        unique=True,
        db_index=True
    )
    order = models.SmallIntegerField(
        'сортировка',
        default=255
    )
    icon = models.ForeignKey(
        Icon,
        verbose_name='иконка',
        on_delete=models.PROTECT,
        default=14
    )
    category = models.CharField(
        'категория услуги',
        choices=CHOICE_CATEGORY,
        max_length=MAX_PREF_LENGTH,
        default='other'
    )
    description = models.TextField(
        'Описание группы услуг',
        max_length=800,
        default='необходимо заполнить',
        help_text='кратко описываем группу услуг'
    )
    active = models.BooleanField(
        'активно',
        default=True
    )
    
    def __str__(self):
        return f"{self.name} ({self.slug})"
    
    def get_icon_url(self):
        return self.icon.get_icon_url()
    
    def icon_html_img(self):
        return mark_safe(
            f'<img src="{self.get_icon_url()}" width="65"/>')
    icon_html_img.short_description = 'Иконка'
    
    # def display_objects(self):
    #     lst = [item.short_name for item in Object.objects.filter(service = self.id) ]
    #     return ' '.join(lst)

class Service(models.Model):
    '''\
        Услуги согласно категории:
        спортивная, секция, прочая '''
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    MAX_NAME_LENGTH = 60
    
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
    typeservice = models.ForeignKey(
        TypeService,
        verbose_name='группа услуг',
        on_delete=models.PROTECT,
        default=1
    )
    
    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={"slug": self.slug})
    
    def get_icon_url(self):
        return self.typeservice.icon.get_icon_url()
    
    def icon_html_img(self):
        return mark_safe(f'<img src="{self.get_icon_url()}" width="65"/>')
    icon_html_img.short_description = 'Иконка'
    
    # def display_objects(self):
    #     lst = [item.short_name for item in Object.objects.filter(service = self.id) ]
    #     return ' '.join(lst)
    

class TypeServiceGallery(models.Model):
    '''\
        Галерея фотографий с типами услуг, используется в слайдере'''
    class Meta:
        verbose_name = 'Фотография вида услуг'
        verbose_name_plural = 'Галерея фотографий услуг'
    
    typeservice = models.ForeignKey(
        TypeService,
        verbose_name='Услуга',
        on_delete=models.PROTECT
    )
    photos = models.ForeignKey(
        Image,
        verbose_name='фотографии',
        on_delete=models.PROTECT
    )
    
    def get_html_photo(self):
        return self.photos.thumbnail_html()
    get_html_photo.short_description = 'фото'
    
    def get_name(self):
        return self.typeservice.name
    get_name.short_description = 'имя'

    def get_img_size(self):
        return self.photos.get_img_size()
    get_img_size.short_description = 'размер'
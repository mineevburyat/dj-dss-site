from django.db import models
from django.urls import reverse
from common.utils import translite
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Object(models.Model):
    '''\
        Информация о объектах дирекции
        название, адрес, геометка
    '''
    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    MAX_SHORT_NAME = 15
    MAX_LONG_NAME = 250

    short_name = models.CharField(
        'краткое имя',
        max_length=MAX_SHORT_NAME,
        help_text=f'Короткое имя объекта (не более {MAX_SHORT_NAME} символов)'
    )
    name = models.CharField(
        'официальное имя',
        max_length=MAX_LONG_NAME,
        help_text=f'Полное официальное имя (не более {MAX_LONG_NAME}  символов)'
    )
    slug = models.SlugField(
        'slug имя в url',
        unique=True,
        db_index=True,
        max_length=MAX_SHORT_NAME,
        help_text='только латинские буквы и цифры'
    )
    address = models.CharField(
        'адрес',
        max_length=200,
        help_text='Адрес по форме город, улица, дом'
    )
    description = RichTextUploadingField(
        'краткое описание', 
        max_length=1000,
        blank=True,
        null=True
    )
    icon = models.ImageField(
        'пиктограмка',
        upload_to='objects',
        blank=True,
        null=True
    )
    photo = models.ImageField(
        'фотография объекта',
        help_text='в будущем набор фотографий для слайдера',
        upload_to='objects',
        blank=True,
        null=True
    )
    # subunit = models.ForeignKey(
    #     'Subunit',
    #     on_delete=models.PROTECT,
    #     null=True,
    #     blank=True,
    #     verbose_name='Подразделение'
    # )

    def __str__(self):
        return f'{self.short_name} ({self.name})'
    
    # def get_absolute_url(self):
        # return reverse('objects:detail_obj', kwargs={"slug": self.slug})
    
class Resource(models.Model):
    '''\
        Ресурсы: тренажерный зал, футбольное поле'''
    class Meta:
        verbose_name = 'Спортивный ресурс'
        verbose_name_plural = 'Спортивные ресурсы'
        
    name = models.CharField(
        'название',
        max_length=25,
        help_text='стадион, универсальный зал и пр.'
    )
    slug = models.SlugField(
        'slug имя в url',
        unique=True,
        db_index=True,
        max_length=25,
        help_text='желательно английское название'
    )
    icon = models.ImageField(
        'пиктограмка',
        upload_to='objects',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f'{self.name} ({self.slug})'
    
class Subunit(models.Model):
    '''\
        Подразделения объекта: бассейн, тренажерка, зал, поле, аренда.
        С конкретными характеристиками, расписанием и контактами'''
    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
    MAX_LENGTH_NAME = 35
    name = models.CharField(
        'название конкретного ресурса',
        max_length=MAX_LENGTH_NAME,
        help_text='подразделение, отдел, направление'
    )
    slug = models.SlugField(
        'slug имя в url',
        unique=True,
        db_index=True,
        max_length=MAX_LENGTH_NAME,
        help_text='только латинские буквы и цифры'
    )
    description = RichTextUploadingField(
        'Описание подразделения, характеристики',
        max_length=1000,
        blank=True,
        null=True
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.PROTECT,
        default=None,
        null=True,
        blank=True,
        verbose_name='спортивный ресурс'
    )
    photo = models.ImageField(
        'фотография',
        help_text='в будущем набор фотографий для слайдера',
        upload_to='objects',
        blank=True,
        null=True
    )
    obj = models.ForeignKey(
        Object,
        verbose_name='Объект',
        on_delete=models.PROTECT,
        default=None,
        null=True,
        blank=True
    )
    contact = models.CharField(
        'Телефон',
        help_text='по сути объект с названием типом связи и пр. возможно несколько',
        max_length=25
    )
    shedule = models.CharField(
        'график работы',
        help_text='режим работы, график, сан. день (как календарь)',
        max_length=25
    )
    
    def __str__(self):
        return f'{self.name} ({self.slug}) на {self.obj}'
    # def get_absolute_url(self):
    #     return reverse('objects:detail_sub', kwargs={"slug": self.slug})
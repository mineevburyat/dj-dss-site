from django.db import models
from django.urls import reverse
from common.utils import translite
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from app_mediafiles.models import Icon, Image
import random
# from app_services.models import TypeService
# Create your models here.

class Object(models.Model):
    '''\
        Информация о объектах
        название, адрес, геометка.
        Выводиться в меню как название и иконка, ранжируется по важности
    '''
    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    MAX_SHORT_NAME = 20
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
        max_length=3000,
        blank=True,
        null=True
    )
    icon_lib = models.ForeignKey(
        Icon,
        verbose_name='иконка',
        on_delete=models.PROTECT,
        default=14
    )
    order = models.SmallIntegerField(
        'Сортировка',
        default=100,
    )
    # type_stock = models.ManyToManyField(
    #     'TypeStock',
    #     verbose_name='группа ресурсов',
    #     help_text='имеющиеся на объекте типы ресурсов',
    # )
    call_center = models.CharField(
        'номер телефона',
        max_length=20,
        default='+7(3012) 5-30-36')

    def __str__(self):
        return f'{self.short_name} ({self.name})'
    
    def get_icon_url(self):
        if self.icon_lib:
            return self.icon_lib.get_icon_url()
    
    def icon_html_img(self):
        return mark_safe(
            f'<img src="{self.get_icon_url()}" width="50" height="50" />')
    icon_html_img.short_description = 'Иконка'
    
    def get_types_stocks(self):
        res = []
        for item in self.type_stock.all():
            res.append(item)
        return res
    # def get_absolute_url(self):
        # return reverse('objects:detail_obj', kwargs={"slug": self.slug})
    
    def get_random_photo(self):
        photos = []
        for gallery in ObjectGallery.objects.filter(obj=self):
            photos.append(
                {'url': gallery.photos.get_url_middle_img(),
                 'alt': gallery.photos.title}
            )
        if photos:
            return random.choice(photos)
        
    def get_contacts_list(self):
        contacts = self.contacts.all()
        return contacts
    
            
    
class TypeStock(models.Model):
    '''\
        Типы материального фонда для меню: категорирование имеющихся материальных ресурсов. То что можно сдать в аренду, забронировать. Выводиться в меню в виде названия и иконки, можно ранжировать по важности'''
    class Meta:
        verbose_name = 'Тип ресурса'
        verbose_name_plural = 'Типы ресурсов'
        
    name = models.CharField(
        'название',
        max_length=35,
        help_text='стадион, универсальный зал и пр. без конкретики'
    )
    slug = models.SlugField(
        'slug имя в url',
        unique=True,
        db_index=True,
        max_length=25,
        help_text='желательно английское название'
    )
    icon = models.ForeignKey(
        Icon,
        verbose_name='файл иконки',
        on_delete=models.PROTECT
    )
    order = models.IntegerField(
        'сортировка',
        default=100
    )
    description = RichTextUploadingField(
        'краткое описание',
        max_length=1500,
        default=''
    )
    obj = models.ForeignKey(
        Object,
        verbose_name='Объект',
        on_delete=models.PROTECT,
        related_name='typestocks',
        blank=True,
        null=True
    )
    # typestock = models.ForeignKey(
    #     TypeService,
    #     verbose_name='группа услуг',
    #     on_delete=models.PROTECT,
    #     related_name='typestock',
    #     blank=True,
    #     null=True
    # )
    
    def __str__(self):
        return f'{self.name} ({self.slug})'
    
    def get_icon_url(self):
        if not self.icon:
            return '/media/emptyicon.png'
        return self.icon.get_icon_url()
    
    def icon_html_img(self):
        return mark_safe(
            f'<img src="{self.get_icon_url()}" width="50" height="50" />')
    icon_html_img.short_description = 'Иконка'
    
    
class Subunit(models.Model):
    '''\
        Конкретный ресурс со своими характеристиками и расписанием бронирования: дорожка бассейна, тренажерка, зал, поле, площадь для аренды.
        С конкретными характеристиками, расписанием и контактами'''
    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'
    MAX_LENGTH_NAME = 45
    name = models.CharField(
        'название конкретного ресурса',
        max_length=MAX_LENGTH_NAME,
        help_text='дрожка бассейна №1, мини-поле №2'
    )
    slug = models.SlugField(
        'slug имя в url',
        unique=True,
        db_index=True,
        max_length=MAX_LENGTH_NAME,
        help_text='только латинские буквы и цифры'
    )
    description = RichTextUploadingField(
        'Описание ресурса, характеристики',
        max_length=1000,
        blank=True,
        null=True
    )
    resource = models.ForeignKey(
        TypeStock,
        on_delete=models.PROTECT,
        default=None,
        null=True,
        blank=True,
        verbose_name='тип ресурса'
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
        help_text='ссылки на контакт TODO',
        max_length=25,
        blank=True,
        null=True
    )
    shedule = models.CharField(
        'график работы',
        help_text='режим работы, график, сан. день (как календарь)',
        max_length=25,
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f'{self.name} ({self.slug}) на {self.obj}'
    # def get_absolute_url(self):
    #     return reverse('objects:detail_sub', kwargs={"slug": self.slug})
    
# class ObjectPhoto(models.Model):
#     '''\
#         Связь объекта с его фотографиями'''
#     class Meta:
#         verbose_name = 'Фотография объекта'
#         verbose_name_plural = 'Фотографии объектов'
    
#     obj = models.ForeignKey(
#         Object,
#         verbose_name='Объект',
#         on_delete=models.PROTECT,
#     )
#     photos = models.ManyToManyField(
#         Image,
#         verbose_name='фотографии',
#         blank=True
#     )
    
class ObjectGallery(models.Model):
    '''\
        Галерея фотографий с объектами'''
    class Meta:
        verbose_name = 'Галерея фотографий объекта'
        verbose_name_plural = 'Галереи фотографий объектов'
    
    obj = models.ForeignKey(
        Object,
        verbose_name='Объект',
        on_delete=models.PROTECT,
        related_name='gallery'
    )
    photos = models.ForeignKey(
        Image,
        verbose_name='фотографии',
        on_delete=models.PROTECT
    )

    def get_html_photo(self):
        return self.photos.thumbnail_html()
    get_html_photo.short_description = 'фото'
    
    def get_short_name(self):
        return self.obj.short_name
    get_short_name.short_description = 'имя'

    def get_img_size(self):
        return self.photos.get_img_size()
    get_img_size.short_description = 'размер'
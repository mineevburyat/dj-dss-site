from django.db import models
from django.urls import reverse
# from common.utils import translite
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from app_mediafiles.models import Icon, Image
import random
# from app_services.models import TypeService
# from app_contacts.models import Contact
import logging
logger = logging.getLogger(__name__)

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
    start_date = models.DateField(
        'дата ввода в эксплуатацию',
        null=True,
        blank=True
    )
    square = models.CharField(
        'площадь',
        max_length=11,
        default='-'
    )
    call_center = models.CharField(
        'номер телефона',
        max_length=20,
        default='+7(3012)')

    def __str__(self):
        return f'{self.short_name} ({self.name})'

    def get_icon_url(self):
        if self.icon_lib:
            return self.icon_lib.get_icon_url()

    def icon_html_img(self):
        return mark_safe(
            f'<img src="{self.get_icon_url()}" width="50" height="50" />')
    icon_html_img.short_description = 'Иконка'

    def get_areas(self):
        return self.sportarea.all()

    def get_absolute_url(self):
        return reverse('objects:detail_obj', kwargs={"slug": self.slug})

    def get_random_photo(self):
        photos = []
        obj_galery = ObjectGallery.objects.get(obj=self)
        for photo in obj_galery.photos.all():
            photos.append(
                {'url': photo.get_url_middle_img(),
                 'alt': photo.alt_txt}
            )
        if photos:
            return random.choice(photos)

    def get_num_areas(self):
        return self.sportarea.all().count()
    get_num_areas.short_description = 'спортплощадок'

    def get_num_vacancy(self):
        return '0'
    
    def get_phones(self):
        phones = []
        for area in self.get_areas():
            for phone in area.get_phones():
                phones.append(phone)
        return phones

class SportArea(models.Model):
    '''\
        Спортивная площадка на объекте'''
    class Meta:
        verbose_name = 'спортплощадка'
        verbose_name_plural = 'спортплощадки'

    name = models.CharField(
        'название',
        max_length=35,
        help_text='бассейн, стадион, тренажерный зал, универсальный зал и пр.'
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
        default='',
        help_text='описание спортплощадки без характеристик и расписания'
    )
    obj = models.ForeignKey(
        Object,
        verbose_name='Объект',
        on_delete=models.PROTECT,
        related_name='sportarea',
        blank=True,
        null=True
    )
    inviting_mes = models.CharField(
        'слоган или призыв к посещению',
        max_length=90,
        default='призывной призыв или слоган'
    )
    characteristics = models.JSONField(
        'характеристики спортплощадки',
        blank=True,
        null=True
    )

    def __str__(self):
        short_name_obj = self.obj.short_name if self.obj else '-'
        return f'{self.name} ({short_name_obj})'

    def get_icon_url(self):
        if not self.icon:
            return '/media/emptyicon.png'
        return self.icon.get_icon_url()

    def icon_html_img(self):
        return mark_safe(
            f'<img src="{self.get_icon_url()}" width="50" height="50" />')
    icon_html_img.short_description = 'Иконка'
    
    def get_random_photo(self):
        photos = []
        area_galery = SportAreaGallery.objects.get(sportarea=self)
        for photo in area_galery.photos.all():
            photos.append(
                {'url': photo.get_url_middle_img(),
                 'alt': photo.alt_txt}
            )
        if photos:
            return random.choice(photos)
    
    def get_phones(self):
        if hasattr(self, 'contact_area'):
            return self.contact_area.phone_set.all()
        else:
            logger.warning(f"{self} не имеет контактов")
            return []
        
    def get_services(self):
        return self.service_set.all()
        
        
class ObjectGallery(models.Model):
    '''\
        Галерея фотографий объектов'''
    class Meta:
        verbose_name = 'фотография объекта'
        verbose_name_plural = 'фотографии объектов'

    obj = models.ForeignKey(
        Object,
        verbose_name='Объект',
        on_delete=models.PROTECT,
        related_name='gallery',
        unique=True
    )
    photos = models.ManyToManyField(
        Image,
        verbose_name='фотографии',
    )

    def __str__(self):
        return f'фото {self.obj.short_name}'
    
    def get_count_photos(self):
        return self.photos.all().count()
    get_count_photos.short_description = 'фотографий'

    def get_short_name(self):
        return self.obj.short_name
    get_short_name.short_description = 'имя'


class SportAreaGallery(models.Model):
    '''\
        Галерея фотографий спортплощадок'''
    class Meta:
        verbose_name = 'фотография спортплощадки'
        verbose_name_plural = 'фотографии спортплощадок'

    sportarea = models.ForeignKey(
        SportArea,
        verbose_name='спортплощадка',
        unique=True,
        on_delete=models.PROTECT
    )
    photos = models.ManyToManyField(
        Image,
        verbose_name='фотографии',
    )

    def __str__(self):
        area_name = self.sportarea.name
        obj_name = self.sportarea.obj.short_name
        return f'{area_name} ({obj_name})'
    
    def get_count_photos(self):
        return self.photos.all().count()
    get_count_photos.short_description = 'фотографий'

    def get_object(self):
        return self.sportarea.obj
    get_object.short_description = 'объект'

    

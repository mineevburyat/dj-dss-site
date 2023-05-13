from django.db import models
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
    # contacts = models.CharField(
    #     'контакты', 
    #     max_length=200
    # )
    # category = models.ForeignKey(
    #     BaseCategory, 
    #     verbose_name='Категория',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True
    # )
    # service = models.ManyToManyField(
    #     Service,
    #     help_text='выберите доступные на объекте спортивные и прочие услуги, спортивные секции. ',
    #     null=True,
    #     blank=True
    # )

    def __str__(self):
        return f'{self.short_name} ({self.name})'
    
    def save(self, *args, **kwargs):
        self.slug = translite(self.short_name)
        super(self).save(*args, **kwargs)

    # def display_service(self):
    #     '''Показать привязанные к объекту услуги (спортивные и прочие)'''
    #     serv_lst = [service for service in self.service.all() if service.category.id == 2 or service.category.id == 299]
    #     return ', '.join([service.name for service in self.service.all()])
    # display_service.short_description = 'Услуги'

    # def display_sportsection(self):
    #     '''Показать привязанные к объекту спортивные секции'''
    #     serv_lst = [service for service in self.service.all()]
    #     return ', '.join([item.name for item in serv_lst if item.category.id == 259])
    # display_sportsection.short_description = 'Спортивные секции'

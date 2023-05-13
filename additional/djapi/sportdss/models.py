from django.db import models
from django.utils import timezone
import re

from ckeditor_uploader.fields import RichTextUploadingField

# class ObjectsDSS(models.Model):
#     class Meta:
#         verbose_name = 'Объект, подразделение'
#         verbose_name_plural = 'Объекты, подразделения'

#     MAX_SHORT_NAME = 50
#     MAX_LONG_NAME = 250
#     '''реквизиты, адрес, геометка, руководство и контакты,
#     список услуг, аренда площадей, рекламные поверхности, список фотографий '''
#     short_name = models.CharField(
#         'краткое имя', 
#         max_length=MAX_SHORT_NAME
#     )
#     long_name = models.CharField(
#         'официальное имя', 
#         max_length=MAX_LONG_NAME
#     )
#     operation_date = models.DateTimeField(
#         'дата начала эксплуатации'
#     )
#     address = models.CharField(
#         'адрес', 
#         max_length=200
#     )

#     def __str__(self):
#         return self.short_name

# class Requisites(models.Model):
#     class Meta:
#         verbose_name = 'Реквизиты подразделения'
#         verbose_name_plural = 'Список реквизитов подразделений (объектов)'
#     '''Режим работы, адрес, телефон, email, интернет приемная, 
#     раскрытие информации, список документов, ИНН КПП, банк, 
#     р.счет и кор счет

#     '''
#     inn = models.CharField(
#         'ИНН', 
#         max_length=10
#     )
#     kpp = models.CharField(
#         'КПП', 
#         max_length=10
#     )

class BaseCategory(models.Model):
    '''\
        Основные категории
        Пункты главного меню'''
    class Meta:
        verbose_name = 'Категория (пункт меню)'
        verbose_name_plural = 'Категории (пункты меню)'
    id = models.PositiveIntegerField(
        'id категории',
        unique=True,
        primary_key=True
    )
    title = models.CharField(
        'старое название',
        max_length=25
    )
    newname = models.CharField(
        'новое название',
        max_length=25,
        null=True,
        blank=True
    )
    slug = models.CharField(
        'Слуг для url',
        max_length=15,
        help_text='краткое название пути в url',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.newname} ({self.title})'

    def get_submenu(self):
        if self.id == 2 or self.id == 259 or self.id == 299:
            lst = [item for item in Service.objects.all() if item.category.id == self.id]
        elif self.id == 335:
            lst = [item for item in About.objects.all()]
        elif self.id == 7632:
            lst = [item for item in Object.objects.all()]
        else:
            lst = []
        return lst

class Service(models.Model):
    '''\
        Точка входа о услугах и секциях.
        спортивная услуга реализуемая на объекте, правила, тарифы, регламент работы
        запись, покупка, бронирование '''
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
    name = models.CharField(
        'название услуги', 
        max_length=60
    )
    descriprion = RichTextUploadingField(
        'краткое описание', 
        max_length=1000
    )
    category = models.ForeignKey(
        BaseCategory, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name}"

    def display_objects(self):
        lst = [item.short_name for item in Object.objects.filter(service = self.id) ]
        return ' '.join(lst)

    
class About(models.Model):
    '''\
        Точка входа подробной информации о предприятиях
        Информация о предприятии, контакты, документы, 
        раскрытие информации, руководство, обратная связь
        новостная лента по предприятиям и услугам'''
    class Meta:
        verbose_name = 'пункт "о нас"'
        verbose_name_plural = '"О нас"'
    name = models.CharField(
        'название подраздела', 
        max_length=60
    )
    description = RichTextUploadingField(
        'краткое описание', 
        max_length=1000
    )
    category = models.ForeignKey(
        BaseCategory, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.name}"

class WorkingMode(models.Model):
    '''\
        Режим работы для контактов'''
    class Meta:
        verbose_name = 'режим работы'
        verbose_name_plural = 'режимы работ'
    mode = RichTextUploadingField(
        'режим работы', 
        max_length=300,
    )
    contact = models.ForeignKey(
        'Contact',
        verbose_name='Контакт',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        txt = re.sub(r'\<[^>]*\>', '', self.mode)
        txt = txt.replace('&mdash;', '-')
        return f"{self.contact} {txt}"

    def display_mode(self):
        txt = re.sub(r'\<[^>]*\>', '', self.mode)
        txt = txt.replace('&mdash;', '-')
        return f"{txt}"
    display_mode.short_description = "режим работы"
class Phone(models.Model):
    '''\
        Номера телефонов для контактов'''
    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'
    phone = models.CharField(
        'телефонный номер', 
        max_length=60,
        # validators=[
        #      RegexValidator(
        #          regex=u'^[0-9\(\)\-\+,\'\s]+$',
        #          message=u'Это поле может содержать только номер телефона в формате "+7(999)999-99-99"',
        #          code='invalid_symbols'
        #      )
        #  ],
    )
    contact = models.ForeignKey(
        'Contact',
        verbose_name='Контакт',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.contact} {self.phone}"   

class Email(models.Model):
    '''\
        Электронная почта для контактов'''
    class Meta:
        verbose_name = 'электронный адрес'
        verbose_name_plural = 'электронные адреса'
    email = models.EmailField(
        'электронный адрес', 
        max_length=60
    )
    contact = models.ForeignKey(
        'Contact',
        verbose_name='Контакт',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    def __str__(self):
        return f"{self.contact} {self.email}"

class Contact(models.Model):
    '''\
        Контакты объектов, подразделений, менеджеров услуг '''
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
    name = models.CharField(
        'название контакта', 
        max_length=35
    )
    description = models.TextField(
        'описание контакта',
        max_length=100
    )
    about = models.ForeignKey(
        'About',
        verbose_name='"о нас"',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='не выбирать если не надо отображать в пункте меню "о нас - контакты"'
    )
    object = models.ForeignKey(
        'Object',
        verbose_name='Объект',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.description}' 

    def display_phones(self):
        phone_lst = Phone.objects.filter(contact=self.id)
        return ', '.join([phone.phone for phone in phone_lst])
    display_phones.short_description = "телефоны"

    def display_email(self):
        email_lst = Email.objects.filter(contact=self.id)
        return ', '.join([email.email for email in email_lst])
    display_email.short_description = "электронная почта"

class Managment(models.Model):
    '''\
        Руководство подразделения '''
    class Meta:
        verbose_name = 'Руководитель'
        verbose_name_plural = 'Руководители'
    job_title = models.CharField(
        'должность', 
        max_length=60
    )
    full_name = models.CharField(
        'ФИО', 
        max_length=60
    )
    photo = models.ImageField(
        'Фотография',
        null=True,
        blank=True
    )
    object = models.ForeignKey(
        'Object',
        verbose_name='Объект',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    about = models.ForeignKey(
        About, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    contact = models.ForeignKey(
        Contact,
        verbose_name="Контакты",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.job_title} {self.full_name}"

class Document(models.Model):
    '''\
        Документы контакта или объекта.
        Закупки, уставные документы, правила, тарифы и пр. '''
    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    TYPE_DOC = (
        ('status', 'уставные документы'),
        ('tarif', 'расценки'),
        ('contract', 'договор'),
        ('cert', 'сертификаты'),
        ('rules', 'правила'),
        ('reports', 'отчеты'),
        ('purchase', 'закупки'),
        ('work', 'охрана труда'),
        ('tax', 'налоговый вычет'),
    )
    type_doc = models.CharField(
        'тип документа', 
        max_length=10,
        choices=TYPE_DOC,
        blank=True,
        default='reports',
        help_text='выберите тип документа'
    )
    url = models.URLField(
        'ссылка на яндекс диск',

    )


class Page(models.Model):
    '''\
        Страница оформленная в html '''
    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
    
class Object(models.Model):
    '''\
        Точка входа о объектах
        реквизиты, адрес, геометка, руководство и контакты,
        список услуг, список фотографий '''
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
        help_text=f'Ролное официальное имя (не более {MAX_LONG_NAME}  символов)'
    )
    address = models.CharField(
        'адрес', 
        max_length=200,
        help_text='Адрес совместимый с GeoAPI'
    )
    contacts = models.CharField(
        'контакты', 
        max_length=200
    )
    category = models.ForeignKey(
        BaseCategory, 
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    service = models.ManyToManyField(
        Service,
        help_text='выберите доступные на объекте спортивные и прочие услуги, спортивные секции. ',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.short_name} ({self.name})'

    def display_service(self):
        '''Показать привязанные к объекту услуги (спортивные и прочие)'''
        serv_lst = [service for service in self.service.all() if service.category.id == 2 or service.category.id == 299]
        return ', '.join([service.name for service in self.service.all()])
    display_service.short_description = 'Услуги'

    def display_sportsection(self):
        '''Показать привязанные к объекту спортивные секции'''
        serv_lst = [service for service in self.service.all()]
        return ', '.join([item.name for item in serv_lst if item.category.id == 259])
    display_sportsection.short_description = 'Спортивные секции'



# class PageOld(models.Model):
#     '''\
#         Модель перенесеная с вордпресс
#         Все страницы сайта
#     '''
#     class Meta:
#         verbose_name = 'Страница'
#         verbose_name_plural = 'Страницы'
#     title = models.CharField(
#         'title',
#         max_length=100
#     )
#     slug = models.CharField(
#         'slug',
#         max_length=20
#     )
#     excerpt = models.CharField(
#         'контакты',
#         max_length=250,
#     )
#     parent = models.PositiveIntegerField(
#         'id родительской категории'
#     )
#     content = models.CharField(
#         'содержимое',
#         max_length=1000
#     )

# class ASFOld(models.Model):
#     '''\
#         Модель перенесеная с вордпресс
#         Возможно описание карточки
#     '''
#     class Meta:
#         verbose_name = 'Карточка страницы'
#         verbose_name_plural = 'Карточки страниц'

#     description = models.CharField(
#         max_length=100
#     )
#     image_url = models.CharField(
#         max_length=150
#     )
#     short_desc = models.CharField(
#         max_length=200
#     )
#     children_view = models.CharField(
#         max_length=50
#     )

# class ImageMedia(models.Model):
#     '''\
#         Модель перенесеная с вордпресс
#         Слайд-картинки разных размеров
#     '''
#     class Meta:
#         verbose_name = 'Медиа ссылка'
#         verbose_name_plural = 'Медиа ссылки'
#     thumbnail = models.CharField(
#         max_length=100
#     )
#     medium = models.CharField(
#         max_length=100
#     )
#     large = models.CharField(
#         max_length=100
#     )
#     full = models.CharField(
#         max_length=100
#     )
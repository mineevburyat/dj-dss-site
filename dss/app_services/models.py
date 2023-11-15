from django.db import models
from django.urls import reverse
from common.utils import translite
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from app_mediafiles.models import Icon, Image
from app_objects.models import Object, SportArea
import random

# искуственные категории услуг
MAX_PREF_LENGTH = 10
CHOICE_CATEGORY = (
        ('sport', 'Спортивные услуги'),
        ('section', 'Спортивные секции'),
        ('relax', 'Отдых'),
        ('other', 'Прочие услуги'),
    )

# class VariousSport(models.Model):
#     '''\
#         вид спорта: по общероссийской классификации'''
#     class Meta:
#         verbose_name = 'Вид спорта'
#         verbose_name_plural = 'Виды спорта'
#     name = models.CharField(
#         'Название спорта',
#         max_length=60,
#         unique=True
#     )
#     slug = models.CharField(
#         'название на английском',
#         max_length=60,
#         unique=True,
#         db_index=True
#     )
    
#     def __str__(self):
#         return f"{self.name} ({self.slug})"
    
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
    
    def get_random_photo(self):
        photos = []
        for gallery in TypeServiceGallery.objects.filter(typeservice=self):
            photos.append(
                {'url': gallery.photos.get_url_middle_img(),
                 'alt': gallery.photos.title}
            )
        if photos:
            return random.choice(photos)
        
    # def get_typestock_name(self):
    #     if self.area:
    #         return self.area.name
    #     return None

class Service(models.Model):
    '''\
        Услуга привязанная к спортивной площадке и типу услуги  '''
    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    MAX_NAME_LENGTH = 120
    
    name = models.CharField(
        'название услуги',
        max_length=MAX_NAME_LENGTH
    )
    description = RichTextUploadingField(
        'краткое описание',
        max_length=2500
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
    order = models.IntegerField(
        'важность',
        default=100
    )
    
    
    def __str__(self):
        # Детские тарифы
        childs_rates = self.get_rates_count(True)
        childs_discount = self.get_discounts_count(True)
        if childs_rates > 1:
            min_discont = self.get_min_discount(True) if self.get_min_discount(True) else '-'
            child_str = f"(детских {childs_rates} тарифа c {childs_discount} дисконтами от {min_discont} руб.)"
        elif childs_rates == 1:
            rate_name = self.get_rates(True).first().name
            rate_price = self.get_rates(True).first().price
            child_str = f"({rate_name} {rate_price} руб.)"
        else:
            child_str = "(детских нет)"
        # прочие тарифы
        other_rates = self.get_rates_count()
        other_discount = self.get_discounts_count()
        if other_rates > 1:
            min_discont = self.get_min_discount() if self.get_min_discount() else '-'
            other_str = f"(взрослых {other_rates} тарифа c {other_discount} дисконтами от {min_discont} руб.)"
        elif other_rates == 1:
            rate_name = self.servicerate.first().name
            rate_price = self.servicerate.first().price
            other_str = f"({rate_name} {rate_price} руб.)"
        else:
            other_str = "тарифов нет"
        return f"{self.name} {other_str} {child_str}"

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={"slug": self.slug})
    
    def get_icon_url(self):
        return self.typeservice.icon.get_icon_url()
    
    def icon_html_img(self):
        return mark_safe(f'<img src="{self.get_icon_url()}" width="65"/>')
    icon_html_img.short_description = 'Иконка'
    
    def get_rates(self, forchilds=False):
        return self.servicerate.filter(forchild=forchilds)
    
    def get_rates_count(self, forchilds=False):
        return len(self.get_rates(forchilds))
    
    def get_discounts_count(self, forchilds=False):
        return sum([rate.get_discounts_count() for rate in self.get_rates(forchilds)])
    
    def get_min_discount(self, forchilds=False):
        list_price = [(rate.get_min_discont() or 0) for rate in self.get_rates(forchilds)]
        if list_price:
            return min(list_price)
        else:
            return None
    # def get_sportarea(self):
    #     if self.sportarea:
    #         return self.sportarea.name
    #     return None
    
    # def get_object(self):
    #     if self.object:
    #         return self.object.name
    #     return None
    
    # def display_objects(self):
    #     lst = [item.short_name for item in Object.objects.filter(service = self.id) ]
    #     return ' '.join(lst)
    

class Rate(models.Model):
    class Meta:
        verbose_name = 'тариф'
        verbose_name_plural = 'тарифы'
        
    service = models.ForeignKey(
        Service,
        verbose_name='услуга',
        on_delete=models.CASCADE,
        related_name='servicerate'
        )
    name = models.CharField(max_length=60)
    forchild = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(
        max_digits=7, decimal_places=2,
        blank=True,
        null=True
        )
    
    def get_disconts(self):
        return [discount for discount in self.discounts.all()]
    
    def get_discounts_count(self):
        return len(self.get_disconts())
    
    def get_min_discont(self):
        disconts_list = self.get_disconts()
        if disconts_list:
            min_discont = min(discont.get_price() for discont in disconts_list)
        else:
            min_discont = self.price
        return min_discont
    
    def get_list_discounts(self):
        list_discont_name = [discont.name for discont in self.get_disconts()]
        if list_discont_name:
            return ", ".join(list_discont_name)
        else:
            return ''
    
    def __str__(self):
        price = f"({self.price} руб.)" if self.price else ''
        # description = f"({self.description})" if self.description else ''
        count_discont = self.get_discounts_count()
        if count_discont:
            min_discont = self.get_min_discont()
            list_discont_name = self.get_list_discounts()
            discont_info = f"({count_discont} дисконта от {min_discont} руб.: {list_discont_name})"
        else:
            discont_info = ""
        url = reverse('admin:{}_{}_change'.format(self._meta.app_label,  self._meta.model_name),  args=[self.id] )
        return mark_safe(f"<a href='{url}'>{self.name} {price} {discont_info}</a>")

    def get_name(self):
        pass
class Discount(models.Model):
    class Meta:
        verbose_name = 'дисконт'
        verbose_name_plural = 'дисконты'
    rate = models.ForeignKey(
        Rate,
        on_delete=models.CASCADE,
        related_name='discounts')
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=3,
        choices=[('pct', 'Скидка в %'), ('amt', 'Фиксированная стоимость')])
    value = models.DecimalField(
        blank=True, 
        null=True, 
        max_digits=6, 
        decimal_places=2)
    

    def __str__(self):
        return f"{self.name} ({self.type}-{self.value})"
    
    def get_price(self):
        if self.type == 'amt':
            return self.value
        else:
            return self.rate.price - self.rate.price * self.value / 100

# class Child(models.Model):
#     name = models.CharField(max_length=255)
#     rate = models.ForeignKey(
#         Rate,
#         on_delete=models.CASCADE,
#         verbose_name='детский')
    
class Promotion(models.Model):
    class Meta:  
        unique_together = ("start_date", "end_date")
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=255)
    

    def __str__(self):  
        if self.start_date and not self.end_date:  
            return f"{self.start_date} - No end date"  
        elif not self.start_date and self.end_date:
            return f"No start date - {self.end_date}"
        else:
            return "Invalid dates"

class TypeServiceGallery(models.Model):
    '''\
        Галерея фотографий с типами услуг, используется в слайдере'''
    class Meta:
        verbose_name = 'Фотография вида услуг'
        verbose_name_plural = 'Галерея фотографий услуг'
    
    typeservice = models.ForeignKey(
        TypeService,
        verbose_name='Услуга',
        on_delete=models.PROTECT,
        related_name='photo'
    )
    photos = models.ForeignKey(
        Image,
        verbose_name='фотографии',
        on_delete=models.PROTECT,
        related_name='service'
    )
    
    def __str__(self):
        return str(self.typeservice)
    
    def get_html_photo(self):
        return self.photos.thumbnail_html()
    get_html_photo.short_description = 'фото'
    
    def get_name(self):
        return self.typeservice.name
    get_name.short_description = 'имя'

    def get_img_size(self):
        return self.photos.get_img_size()
    get_img_size.short_description = 'размер'
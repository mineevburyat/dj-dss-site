from django.db import models
from app_objects.models import Object, SportArea
from django.utils.safestring import mark_safe

# Create your models here.

class Contact(models.Model):
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
    name = models.CharField(
        'название',
        max_length=65,
        unique=True
    )
    email = models.EmailField(
        'email',
        max_length=50,
        blank=True,
        null=True
    )
    obj = models.ForeignKey(
        Object,
        verbose_name='объект',
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='contacts'
    )
    stock = models.ForeignKey(
        SportArea,
        verbose_name='ресурс',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
        
    def __str__(self):
        return f'{self.name}'
    
    def get_object_str(self):
        if self.obj:
            return self.obj.short_name
        return None
    
    def get_phones_str(self):
        phones = []
        for phone in self.phone_set.all():
            phones.append(phone.get_phone_str())
        if phones:
            return mark_safe(',<br>'.join(phones))
        return None
    get_phones_str.short_description = 'телефоны'
    
class Phone(models.Model):
    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'
    
    phone = models.CharField(
        'телефон',
        max_length=20,
        help_text='отображаемый'
    )
    phone_url = models.CharField(
        'телефон',
        max_length=16,
        help_text='согласно e164',
        default='+7'
    )
    phone_add = models.CharField(
        'добавочный',
        blank=True,
        null=True,
        max_length=5
    )
    contact = models.ForeignKey(
        Contact,
        verbose_name='контакт',
        on_delete=models.CASCADE
    )
    
    def get_phone_str(self):
         phone_add = ''
         if self.phone_add:
             phone_add = f' доб. ({self.phone_add})'
         return f'{self.phone}{phone_add}'
    get_phone_str.short_description = 'представление'
    
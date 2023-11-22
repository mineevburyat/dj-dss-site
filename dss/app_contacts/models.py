from django.db import models
from app_objects.models import Object, SportArea
from django.utils.safestring import mark_safe

# Create your models here.

class Contact(models.Model):
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
    email = models.EmailField(
        'email',
        max_length=50,
        blank=True,
        null=True
    )
    sportarea = models.OneToOneField(
        SportArea,
        verbose_name='спортплощадка',
        on_delete=models.PROTECT,
        unique=True,
        related_name='contact_area'
    )
        
    def __str__(self):
        return f'контакты {self.sportarea.name} ({self.sportarea.obj.short_name})'
    
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
    
    name = models.CharField(
        'пояснение',
        max_length=22,
        help_text='кому попадем',
        default='администратор'
    )
    phone = models.CharField(
        'телефон',
        max_length=20,
        help_text='отображаемый'
    )
    phone_url = models.CharField(
        'url',
        max_length=16,
        help_text='согласно e164 (ссылка)',
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
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        obj = self.contact.sportarea.obj.short_name
        sportarea = self.contact.sportarea.name
        return f"{sportarea} {obj} {self.name} - {self.phone}"
    
    def get_phone_str(self):
         phone_add = ''
         if self.phone_add:
             phone_add = f' доб. ({self.phone_add})'
         return f'{self.phone}{phone_add}'
    get_phone_str.short_description = 'представление'
    
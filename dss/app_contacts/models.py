from django.db import models
from app_objects.models import Object, SportArea
from django.utils.safestring import mark_safe
from app_objects.models import Object, SportArea
# Create your models here.

class ContactManager(models.Manager):
    def dic_object_contacts(self):
        all = self.all()
        result = {}
        for contact in all:
            print(contact)
            obj_name = contact.sportarea.obj.name
            area_name = contact.sportarea.name
            phones = contact.phone_set.all()
            dic_obj = result.get(obj_name)
            if dic_obj:
                dic_area = dic_obj.get(area_name)
                if dic_area:
                    dic_area.union(phones)
                else:
                    dic_obj.update({area_name: phones})
            else:
                result[obj_name] = {area_name: phones}
            print(result)
        return result

class Contact(models.Model):
    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
    
    objects = ContactManager()
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
            return mark_safe(', '.join(phones))
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
    
from django.db import models

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
    phone = models.CharField(
        'телефон',
        max_length=15
    )
    phone_add = models.CharField(
        'добавочный',
        blank=True,
        null=True,
        max_length=5
    )
    email = models.EmailField(
        'email',
        max_length=50,
        blank=True,
        null=True
    )
    
    def __str__(self):
        return f'{self.name} ({self.phone})'
    
    
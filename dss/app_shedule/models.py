from django.db import models

# Create your models here.
class Shedule(models.Model):
    class Meta:
        verbose_name = 'график работы подразделения'
        verbose_name_plural = 'графики работ подразделений'
    name = models.CharField(
        'имя расписания',
        max_length=100,
    )
    opening_house = models.JSONField(
        'время работы',
        help_text='время в json виде, согласно схемы',
    )
    exeption_day = models.JSONField(
        'исключительные дни',
        help_text='перечисляем нерабочие и частично рабочие дни',
    )
    
    def __str__(self):
        return f"график работы {self.name}"
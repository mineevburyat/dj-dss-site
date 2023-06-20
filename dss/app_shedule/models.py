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
    
# # Список дней недели.
# 	DAY_CHOICES = (
# 		('MO', 'Понедельник'),
# 		('TU', 'Вторник'),
# 		('WE', 'Среда'),
# 		('TH', 'Четверг'),
# 		('FR', 'Пятница'),
# 		('SA', 'Суббота'),
# 		('SU', 'Воскресенье'),
# 	)

# 	day = models.CharField(max_length=2, choices=DAY_CHOICES, verbose_name='День недели')
# 	time = models.TimeField(verbose_name='Время занятия')
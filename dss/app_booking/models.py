from django.db import models

# Create your models here.
from app_services.models import Service
from app_user.models import User
from datetime import datetime

def json_default_value():
    return {"start": "08:00", "end": "13:00"}

# class SubunitBooking(models.Model):
#     class Meta:
#         verbose_name = 'бронирование ресурса'
#         verbose_name_plural = 'забронированные ресурсы'
        
#     subunit = models.ForeignKey(
#         Subunit,
#         verbose_name='ресурс',
#         on_delete=models.PROTECT
#     )
#     user = models.ForeignKey(
#         User,
#         verbose_name='пользователь',
#         on_delete=models.PROTECT
#     )
#     checkin_date = models.DateField(
#         verbose_name='дата бронирования',
#         default=datetime.now
#     )
#     time_slot = models.JSONField(
#         verbose_name='время начала и конца бронирования',
#         default=json_default_value
#     )
    
#     def __str__(self) -> str:
#         start = self.time_slot.get('start')
#         end = self.time_slot.get('end')
#         return f"бронь {self.subunit} {self.checkin_date} c {start} по {end} ({self.user})"
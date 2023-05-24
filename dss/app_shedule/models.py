from django.db import models

# Create your models here.
class Shedule(models.Model):
    name = models.CharField(
        'имя расписания',
        max_length=100,
        help_text='режим работы услуги или ресурса'
    )
    opening_house = models.JSONField(
        'время работы',
        help_text='время в json виде, согласно схемы',
    #     default='''
    #     [
    # {
    #     "Mon": true, 
    #     "time_list": [{"start": "07:00", "end": "21:45"}]
    # },
    # {
    #     "Tue": true, 
    #     "time_list": [
    #         {"start": "07:00", "end": "21:45"}
    #     ]
    # },
    # {
    #    "Wed": true, 
    #     "time_list": [
    #         {"start": "07:00", "end": "21:45"}
    #     ]
    # },
    # {
    #     "Tuh": true, 
    #     "time_list": [
    #         {"start": "07:00", "end": "21:45"}
    #     ]
    # },
    # {
    #     "Fr": true, 
    #     "time_list": [
    #         {"start": "07:00", "end": "21:45"}
    #     ]
    # },
    # {
    #     "Sat": true, 
    #     "time_list": [
    #         {"start": "08:15", "end": "21:45"}
    #     ]
    # },
    # {
    #     "Sun": "True", 
    #     "time_list": [
    #         {"start": "08:15", "end": "21:45"}
    #     ]
    # }
    # ]
    #     '''
    )
    exeption_day = models.JSONField(
        'исключительные дни',
        help_text='перечисляем нерабочие и частично рабочие дни',
#         default='''
#         [
#   {"2023-02-06": {"work": false, "reason": "санитарный день", "start": "", "end": ""}},
#   {"2023-03-06": {"work": false, "reason": "санитарный день", "start": "", "end": ""}},
#   {"2023-04-03": {"work": false, "reason": "санитарный день", "start": "", "end": ""}},
#   {"2023-05-04": {"work": false, "reason": "санитарный день", "start": "", "end": ""}},
#   {"2023-06-05": {"work": false, "reason": "санитарный день", "start": "", "end": ""}},
#   {"2023-07-03": {"work": false, "reason": "санитарный день", "start": "", "end": ""}},
#   {"2023-10-02": {"work": false, "reason": "санитарный день", "start": "", "end": ""}},
#   {"2023-10-30": {"work": false, "reason": "санитарный день", "start": "", "end": ""}},
#   {"2023-12-04": {"work": false, "reason": "санитарный день", "start": "", "end": ""}},
#   {"2023-12-29": {"work": false, "reason": "санитарный день", "start": "", "end": ""}},
#   {"2023-05-22": {"work": true, "reason": "важное объявление", "start": "15:45", "end": "21:45"}}
#         ]
#          '''
    )
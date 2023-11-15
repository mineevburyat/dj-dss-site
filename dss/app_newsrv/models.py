from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

MAX_PREF_LENGTH = 10
CHOICE_CATEGORY = (
        ('sport', 'Спортивные услуги'),
        ('section', 'Спортивные секции'),
        ('relax', 'Отдых'),
        ('other', 'Прочие услуги'),
    )

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
    description = models.TextField(
        'краткое описание',
        max_length=500
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
    order = models.IntegerField(
        'важность',
        default=100
    )
    # typeservice = models.ForeignKey(
    #     TypeService,
    #     verbose_name='группа услуг',
    #     on_delete=models.PROTECT,
    #     default=1
    # )
    # object = models.ForeignKey(
    #     Object,
    #     verbose_name='объект',
    #     on_delete=models.CASCADE,
    #     default=None,
    #     null=True,
    #     blank=True,
    #     related_name='services'
    # )
    # sportarea = models.ForeignKey(
    #     SportArea,
    #     verbose_name='спортплощадка',
    #     on_delete=models.PROTECT,
    #     related_name='area_services',
    #     null=True,
    #     blank=True
    # )
    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={"slug": self.slug})
    
    def get_icon_url(self):
        return self.typeservice.icon.get_icon_url()
    
    def icon_html_img(self):
        return mark_safe(f'<img src="{self.get_icon_url()}" width="65"/>')
    icon_html_img.short_description = 'Иконка'
    
    def get_sportarea(self):
        if self.sportarea:
            return self.sportarea.name
        return None
    

class Rate(models.Model):
    class Meta:
        verbose_name = 'тариф'
        verbose_name_plural = 'тарифы'
    service = models.ForeignKey(
        Service,
        verbose_name='услуга',
        on_delete=models.CASCADE,
        related_name='ServiceRate'
        )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Discount(models.Model):
    class Meta:
        verbose_name = 'скидка'
        verbose_name_plural = 'скидки'
    rate = models.ForeignKey(
        Rate,
        on_delete=models.CASCADE,
        related_name='discounts')
    name = models.CharField(max_length=255)
    discount_type = models.CharField(
        max_length=2,
        choices=[('pct', 'Скидка в %'), ('amt', 'Фиксированная стоимость')])
    discount_value = models.DecimalField(
        blank=True, 
        null=True, 
        max_digits=5, 
        decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.discount_value})" 

class Child(models.Model):
    name = models.CharField(max_length=255)
    rate = models.ForeignKey(
        Rate,
        on_delete=models.CASCADE,
        verbose_name='детский')
    
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
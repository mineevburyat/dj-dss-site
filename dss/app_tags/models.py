from django.db import models

# Create your models here.
class Tag(models.Model):
    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
        
    tag = models.CharField(max_length=50)
    def __str__(self):
        return self.tag
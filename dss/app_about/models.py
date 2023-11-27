from django.db import models
from app_objects.models import Object
from app_mediafiles.models import Image
# Create your models here.

class Manager(models.Model):
    '''\
        Руководители объектов и руководитель руководителей'''
    class Meta:
        verbose_name = 'руководитель'
        verbose_name_plural = 'руководители'

    job_title = models.CharField(
        'должность',
        max_length=200,
        help_text='поное название'
    )
    full_name = models.CharField(
        'полное имя',
        unique=True,
        db_index=True,
        max_length=250,
    )
    photo = models.OneToOneField(
        Image,
        verbose_name='фотография',
        on_delete=models.PROTECT
    )
    
    
    def __str__(self):
        return f"{self.full_name}"
    
class VacantManager(models.Manager):
    def dic_object_vacants(self):
        result = {}
        for vacant in self.all():
            obj_name = vacant.obj.name
            obj = vacant.obj
            vacants = self.filter(obj=obj)
            dic_obj = result.get(obj_name)
            if dic_obj:
                print(dic_obj)
                dic_obj.union(vacants)
            else:
                result[obj_name] = vacants
        return result

    
class Vacant(models.Model):
    '''\
        Вакантные места на объектах'''
    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'вакантные места'

    objects = VacantManager()
    
    job_title = models.CharField(
        'должность',
        max_length=200,
        help_text='поное название'
    )
    full_name = models.TextField(
        'описание требований',
        db_index=True,
        max_length=250,
    )
    obj = models.ForeignKey(
        Object,
        verbose_name='объект',
        on_delete=models.PROTECT
    )
        
    def __str__(self):
        return f"{self.job_title} ({self.obj.short_name})"
    
    
class TypeDocument(models.Model):
    class Meta:
        verbose_name = 'тип документа'
        verbose_name_plural = 'типы документов'
    name = models.CharField(
        'название',
        max_length=50
    )
    
    def __str__(self):
        return self.name

class Document(models.Model):
    class Meta:
        verbose_name = 'документ'
        verbose_name_plural = 'документы'
        
    typedoc = models.ForeignKey(
        TypeDocument,
        verbose_name='тип документа',
        on_delete=models.PROTECT
    )
    name = models.CharField(
        'название',
        max_length=250
    )
    file = models.FileField(
        'файл',
        upload_to='files',
        
    )
    @property
    def file_url(self):
        try:
            url = self.file.url
        except:
            url = ''
        return url
        
    def __str__(self):
        return f"{self.name} ({self.typedoc.name})"
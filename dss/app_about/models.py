from django.db import models
from app_objects.models import Object
from app_mediafiles.models import Image
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class GetOrNoneManager(models.Manager):
    """Adds get_or_none method to objects
    """
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

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
    
    
class DocumentManager(models.Manager):
    def dic_documents(self):
        result = {}
        doctype_ids = Document.objects.values_list('typedoc', flat=True).distinct()
        for id in doctype_ids:
            doctype = TypeDocument.objects.get(pk=id)
            result[doctype.name] = Document.objects.filter(typedoc=doctype)
        return result
                
    def only_purchases(self):
        try:
            doctype = TypeDocument.objects.get(name__icontains='закупки')
        except:
            return []
        return Document.objects.filter(typedoc=doctype)
    
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
        
    objects = DocumentManager()
    
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
    old_file_name = models.CharField(
         'имя скаченного файла',
         max_length=200,
         blank=True,
         null=True
    )
    content_type = models.CharField(
        max_length=100,
        verbose_name='тип скаченного файла',
        blank=True,
        null=True
    )
    old_url = models.URLField(
        max_length=250,
        verbose_name='старая ссылка',
        blank=True,
        null=True
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
    
class WP_Page(models.Model):
    class Meta:
        verbose_name = 'страница'
        verbose_name_plural = 'страницы'
    
    objects = GetOrNoneManager()
    
    date = models.DateTimeField(
        'дата создания',
        default=timezone.now()
    )
    slug = models.SlugField(max_length=150)
    template = models.CharField(max_length=50)
    old_link = models.URLField(max_length=500)
    title = models.CharField(max_length=300)
    content = RichTextUploadingField(max_length=3000)
    excerpt = models.TextField(max_length=1500)
    parent = models.ForeignKey(
        'WP_Page',
        verbose_name='родительская страница',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    
    def is_parent(self):
        return bool(self.parent)
    
    def __str__(self):
        return f"{self.id} {self.title} ({self.is_parent()})"
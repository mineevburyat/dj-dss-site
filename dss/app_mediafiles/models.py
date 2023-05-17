from django.db import models
import uuid
from pathlib import Path
from django.conf import settings
from django.utils.safestring import mark_safe


def path_icon_file(instance, filename):
    print(instance._meta.object_name, 
          instance._meta.model_name, 
          instance._meta.model,
          instance._meta.parents,
          instance._meta.pk,
          instance._meta.verbose_name,
          filename)
    extentions = Path(filename).suffix[1:]
    filename = f"{uuid.uuid4()}.{extentions}"
    path = Path('imagelibrary/icon', filename)
    print(path)
    return path
    

class Icon(models.Model):
    """
    Иконка и связанная с иконкой текстовая информация
    """
    class Meta:
        verbose_name = 'Иконка'
        verbose_name_plural = 'Иконки'
    name = models.CharField(max_length=60, default='иконка ...')
    image = models.ImageField(
        upload_to=path_icon_file,
    )
    
    # info = models.OneToOneField(ImageInfo, on_delete=models.CASCADE)

    def get_icon_url(self):
        if not self.image:
            return '/media/emptyicon.png'
        return self.image.url
    
    def icon_html_card(self):
        return mark_safe(
            f'''<div style="box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                transition: 0.3s; width: 150px; margin: 10px">
                    <img src="{self.get_icon_url()}" alt="{self.name}" style="width:100%">
                    <div style="padding: 2px 16px;">
                        <h4><b>{self.name}</b></h4>
                    </div>
                </div>''')
    icon_html_card.short_description = 'Иконка'
    
    def __str__(self):
        return f'{self.name}'
    
class F(models.Model):
    t = models.FieldFile
    f = models.FileField

from app_mediafiles.models import Image as ImageMedia
from django.core.management.base import BaseCommand
from io import BytesIO
from django.core.files.base import ContentFile
from pathlib import Path
from PIL import Image as PImage
from django.db.models.signals import post_save
from django.dispatch import receiver
from app_tags.models import Tag
import json

class Command(BaseCommand):
    help = 'берет из json описание картинки и вносит изменение в модель'
    def handle(self, *args, **kwargs):
        try:
            f = open('fixtures/imagecaption.json')
        except:
            self.stderr.write('not find file!')
            raise
        try:
            datas = json.load(f)
            
        except:
            self.stderr.write('error pars json!')
            raise
        for data in datas:
            id = data.get('pk') - 10000
            try:
                image = ImageMedia.objects.get(id=id)
            except:
                self.stdout.write(f'not find this id {id}')
                continue
            fields = data.get('fields')
            image.title = fields.get('title')
            image.caption = fields.get('caption')
            image.slug = fields.get('slug')
            image.alt_txt = fields.get('alt_txt')
            tags_id_list = fields.get('tags')
            for tag_id in tags_id_list:
                for tag in image.tags.all():
                    if tag.pk == tag_id:
                        continue
                    else:
                        image.tags.add(*Tag.objects.filter(pk=tag_id))
            image.save()
            
        
        

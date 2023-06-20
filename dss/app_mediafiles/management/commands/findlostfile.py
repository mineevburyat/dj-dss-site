from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, localtime
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from app_news.models import ImageMedia
from pathlib import Path
from django.conf import settings
from PIL import Image as PImage
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

class Command(BaseCommand):
    help = 'Печатает потерянные картинки'
    def handle(self, *args, **kwargs):
        images = ImageMedia.objects.all()
        attrs = ['image', 'large', 'medium', 'thumbnail']
        for image in images:
            for attr in attrs:
                notfound_flag = False
                field = getattr(image, attr)
                if field.name:
                    abs_path = os.path.dirname(field.path)
                    filename = os.path.basename(field.path)
                    for root, dirs, files in os.walk(abs_path):
                        if filename not in files:
                            notfound_flag = True
                        break
                    if notfound_flag:
                        print(image.id, field, 'потерян!')
                else:
                    print(image, ' нет поля ', field, (attr))
                    
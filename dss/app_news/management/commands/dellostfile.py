import requests
from app_news.models import News, ImageMedia
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, localtime
from django.core.management.base import BaseCommand
from PIL import Image  
from io import BytesIO  
import uuid
from django.core.files.base import ContentFile
from app_news.models import ImageMedia
from pathlib import Path
from django.conf import settings
from PIL import Image as PImage
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from io import BytesIO
import os

class Command(BaseCommand):
    help = 'Очищает от не используемых в базе картинок'
    def handle(self, *args, **kwargs):
        images = ImageMedia.objects.all()
        attrs = ['image', 'large', 'medium', 'thumbnail']
        info = {}
        for image in images:
            for attr in attrs:
                field = getattr(image, attr)
                if field.name:
                    abs_path = os.path.dirname(field.path)
                    if abs_path not in info:
                        info[abs_path] = [os.path.basename(field.path)]
                    else:
                        filenames = info.get(abs_path)
                        filename = os.path.basename(field.path)
                        if filename not in filenames:
                            filenames.append(filename)
        for path, file_list in info.items():
            os.chdir(path)
            for root, dirs, files in os.walk("."):
                for file in files:
                    if file not in file_list:
                        print(f'удаляю {path} {file}')
                        try:
                            os.remove(file)
                        except:
                            print('почему-то нет')
                            continue
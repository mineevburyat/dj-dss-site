from app_news.models import ImageMedia
from django.core.management.base import BaseCommand
from app_news.models import ImageMedia
import os

class Command(BaseCommand):
    help = 'Очищает нагенерированные миниатюры в элемента БД и TODO сами файлы'
    def handle(self, *args, **kwargs):
        images = ImageMedia.objects.all()
        attrs = ['large', 'medium', 'thumbnail']
        for image in images:
            for attr in attrs:
                field = getattr(image, attr)
                if field.name:
                    if os.path.exists(field.path):
                        os.remove(field.path)
                    setattr(image, attr, None)
                    image.save()

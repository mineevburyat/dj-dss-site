
import requests
from app_news.models import News, MAX_EXCERPT
from app_mediafiles.models import Image as ImageMedia
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, localtime
from django.core.management.base import BaseCommand
import time
import re
from app_news.models import MAX_TITLE, MAX_CONTENT, MAX_EXCERPT

class Command(BaseCommand):
    help = 'Очищает поле exerpt от html тэгов'
    def handle(self, *args, **kwargs):
        regexp = re.compile(r'\<[^>]*\>')
        news = News.objects.all()
        for item in news:
            excerpt = item.excerpt
            print(excerpt, ' - ', end='')
            if excerpt is None or excerpt == '':
                excerpt = 'Lorem ipsum amen amen'
            else:
                excerpt = re.sub(regexp, '', excerpt)
            item.excerpt = excerpt
            print(excerpt)
            item.save()



import requests
from app_news.models import News, MAX_EXCERPT
from app_mediafiles.models import Image as ImageMedia
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, localtime
from django.core.management.base import BaseCommand
import time
import datetime
from app_news.models import MAX_TITLE, MAX_CONTENT, MAX_EXCERPT

class Command(BaseCommand):
    help = 'Очищает поле exerpt от html тэгов'
    def handle(self, *args, **kwargs):
        news = News.objects.all()
        for item in news:
            start_date = item.date_activation
            if not item.valid_until_date:
                end_date = datetime.datetime(start_date.year,12,31,23,59)
                item.valid_until_date = end_date
                item.save()


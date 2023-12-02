from django.core.management.base import BaseCommand
import requests
import json
from app_about.models import WP_Page, TypeDocument, Document
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from bs4 import BeautifulSoup as bs
from django.core.files.temp import NamedTemporaryFile
from django.core import files
from urllib.parse import urlparse

        
class Command(BaseCommand):
    help = 'создаем базу документов из страницы WP'
    def handle(self, *args, **kwargs):
        page = WP_Page.objects.get(id=343)
        soup = bs(page.content, features="html.parser")
        for section in soup.find_all('section', 'elementor-section'):
            if section.h2:
                typedoc = TypeDocument.objects.get_or_create(name=section.h2.text)
            else:
                continue
            for a in section.find_all('a', href=True):
                url = a['href']
                if urlparse(url).netloc == 'disk.yandex.ru':
                    ya_disk_api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'
                    params = {'public_key': url}
                    stream = requests.get(ya_disk_api, params=params, stream=True)
                else:
                    stream = requests.get(url, stream=True)
                if stream.status_code != 200:
                    continue
                temp_file = NamedTemporaryFile(delete=True)
                for block in stream.iter_content(1024 * 8):
                    # If no more file then stop
                    if not block:
                        break
                    # Write image block to temporary file
                    temp_file.write(block)
                file_name = ''
                print(a['href'], a.text)
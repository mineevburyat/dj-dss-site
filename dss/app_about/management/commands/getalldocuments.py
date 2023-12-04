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
from urllib.parse import urlparse, parse_qs
import json
from uuid import uuid4
import re
        
class Command(BaseCommand):
    help = 'создаем базу документов из страницы WP'
    def handle(self, *args, **kwargs):
        page = WP_Page.objects.get(id=343)
        CHUNK_SIZE = 1024 * 8
        soup = bs(page.content, features="html.parser")
        for section in soup.find_all('section', 'elementor-section'):
            if section.h2:
                typedocument, success = TypeDocument.objects.get_or_create(name=section.h2.text)
            else:
                continue
            for a_teg in section.find_all('a', href=True):
                url = a_teg['href']
                title = a_teg.text
                self.stdout.write(f"parse link {title}")
                if urlparse(url).netloc == 'disk.yandex.ru':
                    ya_disk_api = 'https://cloud-api.yandex.net/v1/disk/public/resources/download'
                    params = {'public_key': url}
                    stream = requests.get(ya_disk_api, params=params, stream=True)
                    if stream.status_code != 200:
                        self.stderr.write(f"    - yandex disk error {url} {stream.status_code} {a_teg.text}")
                        continue
                    ya_href = json.loads(stream.text).get('href')
                    href = urlparse(ya_href)
                    old_file_name = parse_qs(href.query).get('filename')[0]
                    extension = (old_file_name.split('.'))[-1]
                    content_type = parse_qs(href.query).get('content_type')[0]
                    self.stdout.write(f"    - success get yandex disk: {old_file_name}")
                    stream = requests.get(ya_href, stream=True)
                elif urlparse(url).netloc == 'drive.google.com':
                    googl_disk = 'https://docs.google.com/uc?export=download'
                    regex = "(?<=/folders/)([\w-]+)|(?<=%2Ffolders%2F)([\w-]+)|(?<=/file/d/)([\w-]+)|(?<=%2Ffile%2Fd%2F)([\w-]+)|(?<=id=)([\w-]+)|(?<=id%3D)([\w-]+)"
                    id = re.search(regex, url)
                    id = id.group(0)
                    stream = requests.get(googl_disk, params={'id': id, 'confirm': 1}, stream=True)
                    if stream.status_code != 200:
                        self.stderr.write(f"    - google disk error {url} {stream.status_code}")
                        continue
                else:
                    stream = requests.get(url, stream=True)
                    if stream.status_code != 200:
                        self.stderr.write(f"    - url error {url} {stream.status_code}")
                        continue
                    self.stderr.write(f'    - i am not known parse this {url}')
                
                
                temp_file = NamedTemporaryFile(delete=True)
                for block in stream.iter_content(CHUNK_SIZE):
                    # If no more file then stop
                    if not block:
                        break
                    # Write image block to temporary file
                    temp_file.write(block)
                temp_file.flush()
                name = f"{uuid4().hex}.{extension}"
                file = files.File(temp_file, name=name)
                doc, success = Document.objects.get_or_create(name=title,
                                                     typedoc=typedocument,
                                                     file=file,
                                                     old_file_name=old_file_name,
                                                     content_type=content_type,
                                                     old_url=url)
                self.stdout.write(f"    - create item {old_file_name} {content_type} ({str(file)})")
                
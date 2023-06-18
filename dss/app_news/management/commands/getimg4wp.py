
import requests
from app_news.models import News, ImageMedia
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, localtime
from django.core.management.base import BaseCommand
from PIL import Image  
from io import BytesIO  
import uuid
from django.core.files.base import ContentFile, File
from django.core.files.images import ImageFile
import json
import time

class Command(BaseCommand):
    help = 'Загружает картинки из WordPress'
    def handle(self, domen='https://admin.dss-sport.ru', *args, **kwargs):
        page = 1
        the_end = False
        
        while not the_end:
            payload = {'page': page}
            try:
                media = requests.get(
                    f'{domen}/wp-json/wp/v2/media', 
                    params=payload)
            except:
                time.sleep(20)
                media = requests.get(
                    f'{domen}/wp-json/wp/v2/media', 
                    params=payload)
            if media.status_code:
                datas = media.json()
            else:
                raise TimeoutError
            print(page, media.headers.get('X-WP-TotalPages'))
            if page >= int(media.headers.get('X-WP-TotalPages')):
                the_end = True
            if type(datas) == dict and datas.get("code"):
                print(datas.get("code"), datas.get("message"))
                break
            
            for data in datas:
                id = data.get('id') + 10000
                exist_flag = False
                images = ImageMedia.objects.all()
                for item in images:
                    if item.id == id:
                        exist_flag = True
                        break
                if exist_flag:
                    continue
                print(id, ':', end=' ')
                slug = data.get('slug')
                title = data.get('title').get('rendered')
                caption = data.get("caption").get('rendered')
                if caption:
                    print("caption is not empty", end=' ')
                alt_text = data.get("alt_text")
                date_public = make_aware(parse_datetime(data.get('date_gmt')))
                media_type = data.get("media_type")
                url = data.get("guid").get("rendered")
                filename = data.get("media_details").get("file")
                print(date_public, media_type, url)
                if not (url and media_type == 'image'):
                    print('нет картинки или не картинка!')
                    continue
                
                try:
                    resp = requests.get(url)
                except:
                    print(f'not open {url}')
                    continue
                if resp.status_code == 200:
                    img_file_size = resp.headers.get("Content-Length")
                    try:
                        img = Image.open(BytesIO(resp.content))
                    except:
                        print('формат не соответсвтвует картинке!')
                        continue
                    width, height = img.size
                    img_mode = img.mode
                    exten = img.format.lower()
                else:
                    print('status code is not valide!')
                    continue
                if filename:
                    filename = filename.replace("/", "-")
                else:
                    filename = f"{uuid.uuid4().hex}.{exten}"
                image = ImageMedia.objects.create(
                    id=id, 
                    title=title,
                    slug=slug,
                    caption=caption,
                    date_public=date_public,
                    alt_txt=alt_text,
                    img_file_size=img_file_size,
                    height=height,
                    width=width,
                    img_mode=img_mode,
                    media_type = exten,
                    image = ImageFile(BytesIO(resp.content), filename)
                )
                # image.image.save(
                #     f"",
                #     ContentFile(resp.content, f"{uuid.uuid4().hex}.{exten}")
                # )
                image.save()
                print('success!')
                
            page += 1
        

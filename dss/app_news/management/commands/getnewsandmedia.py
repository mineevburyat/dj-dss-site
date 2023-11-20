
import requests
from app_news.models import News, MAX_EXCERPT
from app_mediafiles.models import Image as ImageMedia
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, localtime
from django.core.management.base import BaseCommand
import time
import re
from app_news.models import MAX_TITLE, MAX_CONTENT, MAX_EXCERPT
from django.core.exceptions import ObjectDoesNotExist
from app_tags.models import Tag
from PIL import Image  as ImagePIL
from io import BytesIO 
import uuid 
from app_mediafiles.models import MAX_TITLE, MAX_CAPTION, MAX_LEN_FILENAME
from django.core.files.images import ImageFile

regexp = re.compile(r'\<[^>]*\>')
Tag.objects.get_or_create(tag='новость')
tags = Tag.objects.filter(tag='новость')

class Command(BaseCommand):
    help = 'Загружает новости из WordPress'
    def handle(self, domen='https://admin.dss-sport.ru', *args, **kwargs):
        ID_PREFIX = 10000
        path = "/wp-json/wp/v2/posts"
        page = 1
        the_end = False
        while not the_end:
            payload = {'page': page}
            try:
                media = requests.get(
                    f'{domen}{path}', 
                    params=payload)
            except:
                time.sleep(20)
                media = requests.get(
                    f'{domen}{path}', 
                    params=payload)
            if media.status_code:
                datas = media.json()
            else:
                raise TimeoutError
            self.stdout.write(f"{page} из {media.headers.get('X-WP-TotalPages')}")
            if page >= int(media.headers.get('X-WP-TotalPages')):
                the_end = True
            if type(datas) == dict and datas.get("code"):
                self.stdout.write(f"{datas.get('code')} из {datas.get('message')}")
                break
            
            for data in datas:
                id = data.get('id')
                # exist_flag = False
                try:
                    news = News.objects.get(id=id)
                    continue
                except ObjectDoesNotExist:
                    pass
                slug = data.get('slug')
                title = data.get('title').get('rendered')
                content = data.get('content').get('rendered')
                date_public = make_aware(parse_datetime(data.get('date_gmt')))
                date_activation = date_public
                # проверить наличие полей если их нет пропустить добавление в базу
                if not (slug or title or content or date_public):
                    self.stderr.write(f"{id}, {title}, {slug}, {content} - not import!")
                    continue
                # отрывок выудить либо из short_desc либо из exerpt либо первые символы контента без тэо
                excerpt = data.get('excerpt').get('rendered')
                short_desc = data.get('short_desc')
                excerpt = short_desc or excerpt
                
                if excerpt is None or excerpt == '':
                    excerpt = re.sub(regexp, '', content[:MAX_EXCERPT])
                else:
                    excerpt = re.sub(regexp, '', excerpt)
                # получаем привязанную к новости картинку
                media_id = data.get('featured_media')
                if media_id and type(media_id) == int:
                    featured_media = int(media_id)
                else:
                    featured_media = 0
                if featured_media != 0:
                    # проверить есть ли уже такая картинка
                    try:
                        img = ImageMedia.objects.get(id=featured_media)
                        self.stdout.write(f"картинка {featured_media} в базе есть, продолжаем")
                    except ObjectDoesNotExist:
                        # качаем картинку json по картинке
                        self.stdout.write(f"картинки {featured_media} в базе нет, добавляем в базу")
                        img = self.get_image(featured_media)
                else:
                    self.stdout.write('картинка к новости не привязана')
                    img = None
                
                news = News.objects.create(
                    id=id, 
                    title=title[:MAX_TITLE],
                    slug=slug[:MAX_TITLE],
                    content=content[:MAX_CONTENT],
                    date_public=date_public,
                    date_activation=date_activation,
                    excerpt=excerpt[:MAX_EXCERPT],
                    featured_media=img,
                )
                news.tags.add(*tags)
                # news.save()
                self.stdout.write(f"{id} : import success!")
            page += 1
    
    def get_image(self, id, domen='https://admin.dss-sport.ru'):
        try:
            media = requests.get(f'{domen}/wp-json/wp/v2/media/{id}')
        except:
            time.sleep(30)
            media = requests.get(f'{domen}/wp-json/wp/v2/media/{id}')
        if media.status_code:
            media_json = media.json()
            self.stdout.write(f"получен json картинки {id}, разбираем данные")
        else:
            self.stderr.write(f"код получения json {media.status_code}, прервано")
            raise TimeoutError
        
        url = media_json.get("guid").get("rendered")
        media_type = media_json.get("media_type")
        if not url:
            self.stderr.write(f'нет url картинки')
            return None
        if media_type != 'image':
            self.stderr.write(f'это не картинка!')
            return None
        try:
            resp = requests.get(url)
        except:
            self.stderr.write(f'not open {url}')
            return None
        if resp.status_code != 200:
            self.stderr.write('status code is not valide!')
        img_file_size = resp.headers.get("Content-Length")
        try:
            img = ImagePIL.open(BytesIO(resp.content))
        except:
            self.stderr.write('формат не соответсвтвует картинке!')
            return None
        width, height = img.size
        img_mode = img.mode
        exten = img.format.lower()
        filename = f"{uuid.uuid4().hex}.{exten}"
        slug = media_json.get('slug')
        title = re.sub(regexp, '', media_json.get('title').get('rendered'))
        description = media_json.get("description").get("rendered")
        caption = media_json.get("caption").get('rendered')
        caption = re.sub(regexp, '', description or caption)
        alt_text = media_json.get("alt_text") or title
        date_public = make_aware(parse_datetime(media_json.get('date_gmt')))
        
        img_object = ImageMedia.objects.create(
            id=id, 
            title=title[:MAX_TITLE],
            slug=slug[:MAX_TITLE],
            caption=caption[:MAX_CAPTION],
            date_public=date_public,
            alt_txt=alt_text[:MAX_TITLE],
            img_file_size=img_file_size,
            height=height,
            width=width,
            img_mode=img_mode,
            media_type=exten,
            image=ImageFile(BytesIO(resp.content), filename)
        )
        img_object.tags.add(*tags)
        # image.save()
        self.stdout.write('success!')
        return img_object
                

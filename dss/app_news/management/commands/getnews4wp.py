
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
                self.stdout.write(f"{datas.get('code')} {datas.get('message')}")
                break
            
            for data in datas:
                id = data.get('id')
                # exist_flag = False
                try:
                    news = News.objects.get(id=id)
                    continue
                except ObjectDoesNotExist:
                    pass
                # news = News.objects.all()
                # for item in news:
                #     if item.pk == id:
                #         exist_flag = True
                #         break
                # if exist_flag:
                #     continue
                slug = data.get('slug')
                title = data.get('title').get('rendered')
                content = data.get('content').get('rendered')
                date_public = make_aware(parse_datetime(data.get('date_gmt')))
                date_acivation = date_public
                # проверить наличие полей если их нет пропустить добавление в базу
                if not (slug or title or content or date_public):
                    self.stderr.write(f"{id}, {title}, {slug}, {content} - not import!")
                    continue
                # отрывок выудить либо из short_desc либо из exerpt либо первые символы контента без тэо
                excerpt = data.get('excerpt').get('rendered')
                short_desc = data.get('short_desc')
                excerpt = short_desc or excerpt
                regexp = re.compile(r'\<[^>]*\>')
                if excerpt is None or excerpt == '':
                    excerpt = re.sub(regexp, '', content[:MAX_EXCERPT])
                else:
                    excerpt = re.sub(regexp, '', excerpt)
                # получаем привязанную к новости картинку
                media_id = data.get('featured_media')
                if media_id and type(media_id) == int:
                    featured_media = int(media_id)
                else:
                    featured_media = None
                if featured_media != 0:
                    img = ImageMedia.objects.get(id=featured_media)
                else:
                    img = None
                news = News.objects.create(
                    id=id, 
                    title=title[:MAX_TITLE],
                    slug=slug[:MAX_TITLE],
                    content=content[:MAX_CONTENT],
                    date_public=date_public,
                    date_acivation=date_acivation,
                    excerpt=excerpt[:MAX_EXCERPT],
                    featured_media=img,
                )
                tag_new, created = Tag.objects.get_or_create(tag='новость')
                news.tags.add(tag_new)
                news.save()
                self.stdout.write(f"{id} : import success!")
            page += 1
                

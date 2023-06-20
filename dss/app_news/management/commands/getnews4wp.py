
import requests
from app_news.models import News
from app_mediafiles.models import Image as ImageMedia
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, localtime
from django.core.management.base import BaseCommand
import time

from app_news.models import MAX_TITLE, MAX_CONTENT, MAX_EXCERPT

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
            print(page, media.headers.get('X-WP-TotalPages'))
            if page >= int(media.headers.get('X-WP-TotalPages')):
                the_end = True
            if type(datas) == dict and datas.get("code"):
                print(datas.get("code"), datas.get("message"))
                break
            
            for data in datas:
                id = data.get('id') + ID_PREFIX
                exist_flag = False
                news = News.objects.all()
                for item in news:
                    if item.pk == id:
                        exist_flag = True
                        break
                if exist_flag:
                    continue
                print(id, ':', end=' ')
                slug = data.get('slug')
                title = data.get('title').get('rendered')
                content = data.get('content').get('rendered')
                date_public = make_aware(parse_datetime(data.get('date_gmt')))
                if not (slug or title or content or date_public):
                    print(id, title, slug, content, 'not import!')
                    print()
                    continue
                excerpt = data.get('excerpt').get('rendered')
                media_id = data.get('featured_media')
                if media_id and type(media_id) == int:
                    featured_media = int(media_id) + ID_PREFIX
                else:
                    featured_media = None
                if featured_media:
                    img = ImageMedia.objects.get(id=featured_media)
                else:
                    img = None
                news = News.objects.create(
                    id=id, 
                    title=title[:MAX_TITLE],
                    slug=slug[:MAX_TITLE],
                    content=content[:MAX_CONTENT],
                    date_public=date_public,
                    excerpt=excerpt[:MAX_EXCERPT],
                    featured_media=img,
                )
                print('success!')
            page += 1
                

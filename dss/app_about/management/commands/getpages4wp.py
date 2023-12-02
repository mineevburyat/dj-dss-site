from django.core.management.base import BaseCommand
import requests
import json
from app_about.models import WP_Page
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

        
class Command(BaseCommand):
    help = 'копирует все страницы с wordpress'
    def handle(self, domen='https://admin.dss-sport.ru', url='/wp-json/wp/v2/pages', *args, **kwargs):
        self.domen = domen
        self.url = url
        datas = self.get_json_data(None)
        for data in datas:
            page = self.parse_jsonitem_and_create(data)
                    
    def get_json_data(self, id):
        payload = {"page":7}
        id = f'/{id}' if id else ''
        self.stdout.write(f'GET {self.domen}{self.url}{id}')
        try:
            pages = requests.get(f'{self.domen}{self.url}{id}', params=payload)
        except:
            self.stderr.write(f"недоступен {self.domen}{self.url}")
            raise
        if pages.status_code == 200:
            data = pages.json()
            if isinstance(data, list):
                self.stdout.write(f"list contain {len(data)} items")
            else:
                self.stdout.write(f"single item")
        else:
            self.stderr.write(f'статус обращения к {self.domen}{self.url}: {pages.status_code}')
            raise ValueError
        return data
    
    def parse_jsonitem_and_create(self, data):
        id = data.get('id')
        if WP_Page.objects.get_or_none(pk=id):
            self.stdout.write(f"id {id} is exist. Next")
            return None
        self.stdout.write(f"id {id} not is exist. Parse and create...")
        slug = data.get('slug')
        title = data.get('title').get('rendered')
        content = data.get('content').get('rendered')
        excerpt = data.get('excerpt').get('rendered')
        date = make_aware(parse_datetime(data.get('date')))
        template = data.get('template')
        old_link = data.get('link')
        parent_id = data.get('parent')
        if parent_id == 0:
            parent = None
        else:
            parent = WP_Page.objects.get_or_none(pk=parent_id)
            if not parent:
                parent = self.parse_jsonitem_and_create(self.get_json_data(parent_id))
        page = WP_Page.objects.get_or_create(pk=id,
                                slug=slug,
                                title=title,
                                content=content,
                                excerpt=excerpt,
                                date=date,
                                template=template,
                                old_link=old_link,
                                parent=parent)
        self.stdout.write(f"create: {str(page)}")
        # for child in data.get('childrens'):
        #         ch_id = child.get('id')
        #         self.stdout.write(f"find childs id {ch_id}")
        #         child_data = self.get_json_data(ch_id)
        #         page_child = self.parse_jsonitem_and_create(child_data)
        return page
    
    
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
        datas = self.get_json_data(domen, url, id=None)
        for data in datas:
            page = self.parse_jsonitem_and_create(data)
            self.stdout.write(f"create: {str(page)}")
            for child in data.get('childrens'):
                id = child.get('id')
                child_data = self.get_json_data(domen, url, id)
                page_child = self.parse_jsonitem_and_create(child_data)
                self.stdout.write(f"create: {str(page_child)}")
        
                
                
    def get_json_data(self, domen, url, id):
        payload = {}
        id = f'/{id}' if id else ''
        print(f'{domen}{url}{id}')
        try:
            pages = requests.get(f'{domen}{url}{id}', params=payload)
        except:
            self.stderr.write(f"недоступен {domen}{url}")
            raise
        if pages.status_code == 200:
            data = pages.json()
        else:
            self.stderr.write(f'статус обращения к {domen}{url}: {pages.status_code}')
            raise ValueError
        return data
    
    def parse_jsonitem_and_create(self, data):
        id = data.get('id')
        if WP_Page.objects.get_or_none(pk=id):
            return None
        slug = data.get('slug')
        title = data.get('title').get('rendered')
        content = data.get('content').get('rendered')
        excerpt = data.get('excerpt').get('rendered')
        date = make_aware(parse_datetime(data.get('date')))
        template = data.get('template')
        old_link = data.get('link')
        parent = WP_Page.objects.get_or_none(pk=data.get('parent'))
        page = WP_Page.objects.create(pk=id,
                                slug=slug,
                                title=title,
                                content=content,
                                excerpt=excerpt,
                                date=date,
                                template=template,
                                old_link=old_link,
                                parent=parent)
        return page
    
    
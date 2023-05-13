import requests
import json
url = 'https://admin.dss-sport.ru/wp-json/wp/v2/pages/'
category_list = [
        {'id': 2, 'title': 'Спорт'},
        {'id': 299, 'title': 'Отдых'},
        {'id': 335, 'title': 'Дирекция'},
        {'id': 259, 'title': 'Спортивные секции'},
        {'id': 7632, 'title': 'Спортивные объекты'}
]

def get_childrens(obj):
    body = obj.get("childrens", [])
    res = []
    for item in body:
        res.append((item.get("id"), item.get("title")))
    return res

def get_all_children(id, title, url=url):
    resp = requests.get(url + str(id))
    body  = resp.json()
    childs_lst = get_childrens(body)
    
    if not childs_lst:
        return {str(id) + ', ' + title: []}
    else:
        res = []
        for child in childs_lst:
            child_id, child_title = child
            res.append(get_all_children(child_id, child_title))
        return {str(id) + ', ' + title: res}
result = []
for category in category_list:
    result.append(get_all_children(category.get("id"), category.get("title")))
    print(result)
with open('pages.json','w') as f:
    json.dump(result,f,ensure_ascii=False)
# for child in resp.get('childrens'):
#     print(child.get('acf'))

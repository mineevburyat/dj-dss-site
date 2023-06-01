
import requests

post = requests.get(
    'https://admin.dss-sport.ru/wp-json/wp/v2/posts')
if post.status_code:
    print(post.headers.get('X-WP-Total'))
    print(post.headers.get('X-WP-TotalPages'))
    datas = post.json()
    print(len(datas))
    # for data in datas:
    #     print('id', data.get('id'))
    #     print('date', data.get('date'))
    #     print('slug', data.get('slug'))
    #     print('heading', data.get('heading'))
    #     print('short_desc', data.get('short_desc'))
    #     print('title', data.get('title').get('rendered'))
    #     print('content', data.get('content').get('rendered'))
    #     print('excerpt', data.get('excerpt').get('rendered'))
    #     print(data.get('meta_cat'))

# page = 2

# while True:
#     payload = {'per_page': page}
#     post = requests.get(
#         'https://admin.dss-sport.ru/wp-json/wp/v2/posts', 
#         params=payload)
#     if post.status_code:
#         datas = post.json()
#     for data in datas:
#         print('id', data.get('id'))
#         print('date', data.get('date'))
#         print('slug', data.get('slug'))
#         print('heading', data.get('heading'))
#         print('short_desc', data.get('short_desc'))
#         print('title', data.get('title').get('rendered'))
#         print('content', data.get('content').get('rendered'))
#         print('excerpt', data.get('excerpt').get('rendered'))
#         print(data.get('meta_cat'))
    
#     if page >= 1:
#         break
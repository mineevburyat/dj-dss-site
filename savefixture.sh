#! /bin/sh
cd dss
python manage.py dumpdata menu > fixtures/menu.json
python manage.py dumpdata app_mediafiles > fixtures/mediafiles.json
python manage.py dumpdata app_objects > fixtures/objects.json
python manage.py dumpdata app_services > fixtures/servicess.json
python manage.py dumpdata app_contacts > fixtures/contacts.json
python manage.py dumpdata app_shedule > fixtures/shedule.json
python manage.py dumpdata app_piplscard > fixtures/piples.json
python manage.py dumpdata app_user > fixtures/user.json
python manage.py dumpdata app_news > fixtures/news.json

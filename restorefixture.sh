#! /bin/sh
cd dss
python manage.py loaddata fixtures/menu.json
python manage.py loaddata fixtures/mediafiles.json
python manage.py loaddata fixtures/tags.json
python manage.py loaddata fixtures/news.json
python manage.py loaddata fixtures/objects.json
python manage.py loaddata fixtures/servicess.json
python manage.py loaddata fixtures/contacts.json
python manage.py loaddata fixtures/shedule.json
python manage.py loaddata fixtures/piples.json
python manage.py loaddata fixtures/user.json

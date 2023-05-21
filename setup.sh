#! /bin/sh
python manage.py loaddata fixtures/menu.json
python manage.py loaddata fixtures/mediafiles.json
python manage.py loaddata fixtures/objects.json
python manage.py loaddata fixtures/servicess.json
python manage.py loaddata fixtures/contactss.json
python manage.py createsuperuser
python manage.py runserver

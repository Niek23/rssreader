#!/bin/bash
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.com', 'admin')" | python manage.py shell
python manage.py createfeed http://www.nu.nl/rss/Algemeen
python manage.py createfeed https://feeds.feedburner.com/tweakers/mixed
python manage.py runserver 0.0.0.0:8000
#!/bin/bash
cd /data/www/Star
git pull
killall -9 uwsgi
python3 manage.py collectstatic --noinput -c

python3 manage.py compress
python3 manage.py update_index

/usr/local/python3.5/bin/uwsgi uwsgi.ini

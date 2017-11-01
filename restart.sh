#!/bin/bash
cd /data/www/Star
git pull
killall -9 uwsgi
python3 manage.py collectstatic
python3 manage.py compress

killall -9 uwsgi
/usr/local/python3.5/bin/uwsgi uwsgi.ini

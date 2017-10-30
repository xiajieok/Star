#!/bin/bash
cd /data/www/Star
git pull
killall -9 uwsgi

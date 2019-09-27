#!/usr/bin/env bash
service nginx start
uwsgi --ini app.ini
# service nginx restart


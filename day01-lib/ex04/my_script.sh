#!/bin/sh

python3 -m venv django_env
django_env/bin/python3 -m pip install -r requirement.txt
. django_env/bin/activate
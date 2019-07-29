#!/bin/bash -ex

# create venv
python -m venv ./.testenv

# install pip-tools
./.testenv/bin/pip install pip-tools

# install requirements
./.testenv/bin/pip-sync requirements/requirements.txt

# check for migrations
./.testenv/bin/python IRMIS/manage.py makemigrations --check --dry-run

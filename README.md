# ILO Integrated Roads Management System

## Installation

1. git clone this repository and cd into it
2. install Pipenv https://docs.pipenv.org and `pipenv install`
3. we require GEODJANGO support, install and create a `irmis_db` database  
  - see https://docs.djangoproject.com/en/2.2/ref/contrib/gis/ for installation instructions
  - Postgresql is recommended for deployments, sqlite _may_ be possible in development
4. migrate `pipenv run IRMIS/manage.py migrate`
5. create a super user `pipenv run IRMIS/manage.py createsuperuser`
6. run the dev server `pipenv run IRMIS/manage.py runserver`

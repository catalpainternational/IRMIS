# ILO Integrated Roads Management Information System

## Installation

1. git clone this repository using `--recurse-submodules` and cd into it
  - If you forgot to `--recurse-submodules` then `git submodule init && git submodule update`
2. create a python 3.6 virtual environment and install pip-tools `pip install pip-tools`
3. install requirements with `pip-sync requirements/requirements-dev.txt`
4. we require GEODJANGO support, create a `irmis_db` postgresql database with the POSTGIS extension
  - see https://docs.djangoproject.com/en/2.2/ref/contrib/gis/ for installation instructions
5. In your virtual environment run `manage.py migrate` `manage.py createsuperuser` `manage.py runserver`

## Pip-tools

https://pypi.org/project/pip-tools/

When adding python dependencies, add them to `requirements/requirements.in`, do not pin the version
When adding python development dependencies, add them to `requirements/requirements-dev.in`, do not pin the version

Run `pip-compile requirements/requirements.in` to produce `requirements/requirements.txt`
Run `pip-compile requirements/requirements-dev.in` to produce `requirements/requirements-dev.txt`

Use `pip-compile --upgrade` to upgrade versions of libraries, then test the result!

## Set up front-end

1. Install [Yarn](https://yarnpkg.com/en/docs/install).
2. Navigate to the project's root directory and run `yarn` to install dependencies.
3. You can compile SASS and JavaScript assets with `yarn run dev`.
4. Yarn can detect changes in these assets and rebuild them automatically. Use `yarn run watch`.

## How to Import New Features from a Shapefile (.shp)

1. Import the shapefile schema and data - NOTE: This does not import geometries
  1. run `shp2pgsql -d -n path/to/your/.dbf source_table_name` and check the outputted SQL
  2. read the help https://helpmanual.io/help/shp2pgsql/ if you need to make changes
  3. run that sql against your database using `psql` or `manage.py dbshell`: eg `shp2pgsql -d -n ../../ngis/National_Road.dbf source_national_road | ./manage.py dbshell`

2. Create unmanaged model code by using inspectdb
  1. `./manage.py inspectdb source_table_name` this will output some django model code, drop it into models.py
  2. you may have to edit these files to make them managed so that other developers and deployments create the tables
  3. `./manage.py makemigrations`
  4. `./manage.py migrate` - you may have to fake this locally ( as you will have already created the table )

3. Adapt and run the import code in the Importimport.py
  1. Here be dragons, unexpected geometry types, wierd metadata, duplications.

## Pre-Commit (Black formatter)

This repo has been setup with a pre-commit hook for Black formatter. This ensures that your code meets formatting standard prior to commiting to Git. You can read more about it go here: https://pre-commit.com/

If you want to enable it, run the following command in the repo folder, after having pip installed all dev requirements (`requirements-dev.txt`): `pre-commit install`

## Testing

This project uses pytest-django https://pytest-django.readthedocs.io/en/latest/tutorial.html
To run tests cd to the django directory ( next to manage.py ) and type `pytest`
To run tests with debugger breakpoint support use `pytest -s`
To run tests then keep the db, and re-use it next time use `pytest --reuse-db` and the `pytest --create-db` when you have changed models and migrations
To run tests that match a pattern use `-k` e.g. `pytest -k api`

## Geobuf

We use https://github.com/mapbox/geobuf for compressing GeoJson for transfer down the wire.
`./manage.py collate_geometries` will group Road models and merge their geometries into a GeoJson FeatureCollection, then encode it into a geobuf file.
The files are saved in the media root for access by the client.

## Protobuf

We use google protobuf to compress road metadata for transfer down the wire.
https://developers.google.com/protocol-buffers/docs/pythontutorial is the best resource I have found for learning about it.
To make any message schema changes go here https://github.com/protocolbuffers/protobuf/releases/tag/v3.9.1 to find a suitable package for your OS and follow the instructions in the README. Make sure the protoc binary is available on your PATH.
run `yarn protoc` to update the generated python and javascript code.


## Django Reversion

We use the package `django-reversion` to allow us the ability to maintain a historic record of Road model changes, revert to previous states of records, and recovering deleted records.
You can read more on it here: https://django-reversion.readthedocs.io/en/stable/index.html

If you're setting up from a new DB (ie. not copied from staging / production DB), after pip installing django-reversion and running migrations, you should run `./manage.py createinitialrevisions` to create the initial revision for registered models in the project.

## Javascript/Riot translations

See the package.json file for two useful commands to makemessages for javascript and riot
- `yarn collect_gettext` runs a python tool that looks for all places in riot tags where you have used gettext, and puts them in a generated collation file
- `yarn jsmessages` runs the above command AND runs django makemessages with the correct parameters to make po files under the djangojs domain

djangojs messages are delivered to the browser using https://docs.djangoproject.com/en/2.2/topics/i18n/translation#django.views.i18n.JavaScriptCatalog
riot4 tags should use window.gettext('') to access translations

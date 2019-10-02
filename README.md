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

## How to Import Initial data from sources

The initial data for the estrada system  is commited to the repository here https://github.com/catalpainternational/estrada-data-sources
Clone this repository before performing import. It's README contains information about the source of that data and the processes used to create it

**Important**
This entire sequence must be performed to completion before users are allowed to edit the imported features (roads).

1. `./manage.py import_shapefiles ../../path/to/the/data-sources/repo/shapefiles`
  - imports the shapefile geometries and copies properties across where useful

2. `./manage.py import_csv ../../path/to/the/data-sources/repo/csv`
  - copies road attributes from the csv ( from program excel files )

3. `./manage.py set_road_municipalities`
  - sets road administrative areas from the road centroids

4. `./manage.py collate_geometries`
  - you have edited roads so re-collate

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

If you're setting up from a new DB (ie. not copied from staging / production DB), after pip installing django-reversion and running migrations, you need to create the initial revision, for registered models in the project, with the following two commands:

`./manage.py createinitialrevisions assets.road --comment="Import from Shapefile"`
`./manage.py createinitialrevisions`

## Translations

See the package.json file for useful commands to makemessages
- `yarn collect_gettext` runs a python tool that looks for all places in riot tags where you have used gettext, and puts them in a generated collation file
- `yarn jsmessages` runs the above command AND runs django makemessages with the correct parameters to make po files under the djangojs domain
- `yarn djangomessages` runs django makemessages
- `yarn makemessages` runs javascript and django messages

djangojs messages are delivered to the browser using https://docs.djangoproject.com/en/2.2/topics/i18n/translation#django.views.i18n.JavaScriptCatalog
riot4 tags should use window.gettext('') to access translations

## Export Geojson

We've been asked for a simple geojson exports, the `make_geojson` management command is here to help
It currently accepts a mandatory municipality name and outputs geojson on the standard out
usage : `./manage.py make_geojson ainaro > ainaro.json`

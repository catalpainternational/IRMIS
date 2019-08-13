# ILO Integrated Roads Management Information System

## Installation

1. git clone this repository using `--recurse-submodules` and cd into it
  - If you forgot to `--recurse-submodules` then `git submodule init && git submodule update`
2. create a python 3.6 virtual environment and install pip-tools `pip install pip-tools`
3. install requirements with `pip-sync requirements/requirements-dev.txt`
4. we require GEODJANGO support, create a `irmis_db` postgresql database with the POSTGIS extension
  - see https://docs.djangoproject.com/en/2.2/ref/contrib/gis/ for installation instructions
  - Sqlite is possible in development ( using spatiallite )
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

## How to Import New Features from a Shapefile (.shp) and re-build the unmanaged models.

1. Import Shapefiles into the database (2 options available)
  - Using management command (use help (`--help`) for more details) to import and build un-managed madel in 1 step: `./manage.py import_shapefile_features --filename=./Shapefiles_GIS/National_Road.shp`
  - Using `shp2pgsql` command line tool to import and a seperate management command:
      - Import the data into the DB: `shp2psql -I -c -s 32751 ./path/to/file.shp <table_name>`
      - Management command run after import to build an unmanaged model: `./manage.py build_feature_model --table=<table_name>` (table name is "source_" + <shapefile_name>)
2. Remove any bad import GEO data from shapefiles
`./manage.py remove_problematic_features --dryrun=True`

## Testing

Add details of testing here...

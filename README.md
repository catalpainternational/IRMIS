# ILO Integrated Roads Management Information System

## Bemvindu! Let's get setup quickly!

1. Clone this repository, making sure to use the `--recurse-submodules` flag.
2. Clone the  ` estrada-data-sources` repository (https://github.com/catalpainternational/estrada-data-sources) to get source shape files.
3. Create a virtual environment with Python 3.6+.
4. Install [pip-tools](https://pypi.org/project/pip-tools/).
5. Install project `requirements-dev` with pip-tools.
6. Install [Yarn](https://yarnpkg.com/en/docs/install).
7. Install all yarn-managed packages (`yarn`) and compile the JS/CSS files (`yarn dev`).
8. Install the Google Protobuf compiler (for Mac OS, using Homebrew `brew install protobuf` is easiest).
9. Install the POSTGIS extension for Postgresql (https://docs.djangoproject.com/en/3.0/ref/contrib/gis/install/postgis/).
10. Get a copy of the Estrada DB from Production server (https://estrada-production.catalapa.build) and load the DB.
11. Build local geometry files with Django management command `collate_geometries`.
12. Setup cache tables with Django management command `createcachetable`.
13. Run the server.


## Extra Information and Details On Specific Management Commands & Project Technologies Used

## Pip-tools

https://pypi.org/project/pip-tools/

When adding python dependencies, add them to `requirements/requirements.in`, do not pin the version
When adding python development dependencies, add them to `requirements/requirements-dev.in`, do not pin the version

Run `pip-compile requirements/requirements.in` to produce `requirements/requirements.txt`
Run `pip-compile requirements/requirements-dev.in` to produce `requirements/requirements-dev.txt`

Use `pip-compile --upgrade` to upgrade versions of libraries, then test the result!

## Setting up the front-end

1. Install [Yarn](https://yarnpkg.com/en/docs/install).
2. Navigate to the project's root directory and run `yarn` to install dependencies.
3. You can compile SASS and JavaScript assets with `yarn run dev`.
4. Yarn can detect changes in these assets and rebuild them automatically. Use `yarn run watch`.

## How to import initial data from sources

The initial data for the estrada system  is commited to the repository here https://github.com/catalpainternational/estrada-data-sources
Clone this repository before performing import. It's README contains information about the source of that data and the processes used to create it

**Important**
This entire sequence must be performed to completion before users are allowed to edit the imported features (roads).

** Step 1 below has been temporarily disabled while we work on doing a more nuanced per file reimport process. **
** Please use import_shapefile instead.  Note that import_shapefile does not yet support deleting of any previous attempt at importing a file.  It can only be used once. **

1. `./manage.py reimport_shapefiles ../../path/to/the/data-sources/repo/shapefiles <asset_type>`
  - reimports the shapefile geometries and copies properties across where useful (note this does delete all existing assets for the `<asset_type>` being imported)
  - `<asset_type>` is one of "road", "bridge", "culvert", or "drift"
  - also calls `set_municipalities` and `collate_geometries` automatically

2. `./manage.py import_csv ../../path/to/the/data-sources/repo/csv`
  - copies road attributes from the csv ( from program excel files )

3. `./manage.py set_structure_fields`
  - determines the closest road to each structure (bridge, culvert, drift), and sets the `road_id`, `road_code` and `asset_class` to match

### Additional Steps - these are automatically performed after `reimport_shapefiles`
  A. `./manage.py set_unknown_asset_codes`
    - Fixes assets with missing road / structure codes , assigning these roads a unique `XX_` `road_code`, `XB_`/`XC_`/`XD_` `structure_code`.

  B. `./manage.py set_municipalities <optional: "all", "road", "bridge", "culvert" or "drift">`
    - Sets the administrative areas for each asset/structure, based the centroids of their respective geometries
    - Takes an optional argument to restrict the municipalities getting set to objects of a single type
    - If 'all' argument is given all of the assets/structures will have their municipalities set

  C. `./manage.py collate_geometries`
    - you have imported / edited roads, bridges, culverts, drifts, so re-collate

### Additional Step - this is automatically performed by the survey commands below
  D. `./manage.py set_unknown_link_codes`
    - Fixes roads with bad link codes, and tries to set as many `None` link codes to the road's road code if there are no clashes.

    Note: this is not performed by the `survey` commands below if their `--no-road-refresh` option is specified

4. `./manage.py make_road_surveys <optional: --no-road-refresh>`
  - Refresh the calculated Road record geometry data and clean the link codes (unless you specify --no-road-refresh)
  - Then from those Road records recreate all of the 'programmatic' Surveys for Roads, and
  - Refresh all user entered Surveys for Roads

  Note: Refreshing the programmatic Surveys relies on completeness of the Road record geometry data.  Therefore it is recommended to not use the `--no-road-refresh` option unless you've literally just run `make_road_surveys` or `import_traffic_surveys` immediately before.

  Note: This management command is SLOW.  It has to work road_code by road_code so it runs a LOT of queries.

5. `./manage.py import_traffic_surveys ../../path/to/the/traffic/survey/csv <optional: --no-road-refresh>`
  - Refresh the calculated Road record geometry data and clean the link codes (unless you specify --no-road-refresh)
  - Then recreate the programmatic traffic surveys from the csv file

  Note: Refreshing the programmatic traffic Surveys relies on completeness of the Road record geometry data.  Therefore it is recommended to not use the `--no-road-refresh` option unless you've literally just run `make_road_surveys` or `import_traffic_surveys` immediately before.

6. `./manage.py roughness_and_breakpoints`
  - Create (if not existing) Roughness Surveys and...
  - Refresh the Roughness Survey aggregates & Breakpoint relationships

  Note: Should ONLY be run after the appropriate topology load and import commands have been run as well:
    - `loaddata /var/www/estrada/estrada-data-sources/topology/fixtures/topology.estradaroad.json`
    - `init_topology_functions`
    - `import_csv_source roughness /var/www/estrada/estrada-data-sources/csv/<file-path>.csv`

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
`./manage.py collate_geometries` will group Road, Bridge, Culvert & Drift asset models and merge their geometries into a GeoJson FeatureCollection, then encode it into a geobuf file.
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

## Periodic / Conditional Tasks

### Set Structure Fields

This command updates certain fields on the Bridge, Culvert and Drift models that relate to the road the bridge, culvert or drift is closest to. This is necessary as these models have a weak reference to a Road ID. This command does a nearest neighbour search and sets `road_id`, `asset_class` and `road_code` based on the nearest matching road.
```
./manage.py set_structure_fields
```

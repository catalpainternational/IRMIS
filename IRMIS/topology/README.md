# Topologies App

Topologies are a different, more machine-oriented way of viewing geographic data. They're helpful in situations where you want to have certain rules in place such as "lines should connect", "lines should not overlap", "lines should break into parts at intersections".

This app includes a table of "fixes" for geometries which are terribly bad and some code to fix up geometries which are only a little bit bad. The result is a polulated table of ONE road code with THE linestring defining that road.

## Loading Estrada Roads

(dumpdata from some source where already ran):

```
./manage.py loaddata estradaroad.json
```

## Recreate Topology

This app includes a management command to "make topology". This will probably not work well unless the "RoadCorrection" table is also popluated. This has revised geometries where the source data had gaps, overlaps, duplicates etc.

```
./manage.py migrate
./manage.py loaddata roadcorrection.json
./manage.py make_topology
```

## To Do

-   Move exclusion IDs from the SQL into a separate table

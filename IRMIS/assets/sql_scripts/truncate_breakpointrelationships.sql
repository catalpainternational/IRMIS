COMMIT;
TRUNCATE assets_breakpointrelationships CASCADE;
SELECT setval(pg_get_serial_sequence('assets_breakpointrelationships','id'),  coalesce(max("id"), 1), max("id") IS NOT null) FROM assets_breakpointrelationships;
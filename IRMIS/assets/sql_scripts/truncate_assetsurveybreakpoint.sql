COMMIT;
TRUNCATE assets_assetsurveybreakpoint CASCADE;
SELECT setval(pg_get_serial_sequence('assets_assetsurveybreakpoint','id'),  coalesce(max("id"), 1), max("id") IS NOT null) FROM assets_assetsurveybreakpoint;


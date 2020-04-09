	-- These sometimes have links to survey.
BEGIN;
	TRUNCATE assets_assetsurveybreakpoint CASCADE;
	TRUNCATE assets_breakpointrelationships CASCADE;
	-- Zero the id's
	SELECT setval(pg_get_serial_sequence('assets_assetsurveybreakpoint','id'),  coalesce(max("id"), 1), max("id") IS NOT null) FROM assets_assetsurveybreakpoint;
	SELECT setval(pg_get_serial_sequence('assets_breakpointrelationships','id'),  coalesce(max("id"), 1), max("id") IS NOT null) FROM assets_breakpointrelationships;
	-- Clear all "aggregate_roughness" surveys
COMMIT;
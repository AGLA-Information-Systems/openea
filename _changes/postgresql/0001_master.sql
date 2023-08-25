\i _changes/postgresql/0001_organisation.sql
\i _changes/postgresql/0001_profile.sql
\i _changes/postgresql/0001_task.sql
\i _changes/postgresql/0001_log.sql

-- DELETE FROM django_migrations;
DROP TABLE webapp_organisation;
DROP TABLE webapp_profile;
DROP TABLE webapp_task;
DROP TABLE webapp_log;

COMMIT;
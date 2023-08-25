.read "_changes/sqlite/0001_organisation.sql"
.read "_changes/sqlite/0001_profile.sql"
.read "_changes/sqlite/0001_task.sql"
.read "_changes/sqlite/0001_log.sql"

-- DELETE FROM django_migrations;
DROP TABLE webapp_organisation;
DROP TABLE webapp_profile;
DROP TABLE webapp_task;
DROP TABLE webapp_log;

COMMIT;
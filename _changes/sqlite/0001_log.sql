CREATE TABLE "organisation_log_2" ("id" char(32) NOT NULL PRIMARY KEY, "source" varchar(1024) NOT NULL, "target" char(32) NULL, "details" text NULL, "timestamp" datetime NULL, "user" char(32) NULL, "organisation_id" char(32) NULL REFERENCES "organisation_organisation" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO organisation_log_2 SELECT * FROM organisation_log;
DROP TABLE organisation_log;
ALTER TABLE organisation_log_2 RENAME TO organisation_log;

CREATE INDEX IF NOT EXISTS "organisation_log_organisation_id_c13f8621" ON "organisation_log" ("organisation_id");
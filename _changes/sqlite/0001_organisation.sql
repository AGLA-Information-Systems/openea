CREATE TABLE "organisation_organisation_2" ("id" char(32) NOT NULL PRIMARY KEY, "name" varchar(1024) NOT NULL, "location" varchar(1024) NOT NULL, "description" text NULL, "is_active" bool NOT NULL, "created_at" datetime NULL, "modified_at" datetime NULL, "deleted_at" datetime NULL, "created_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "deleted_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "modified_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO organisation_organisation_2 SELECT * FROM organisation_organisation;
DROP TABLE organisation_organisation;
ALTER TABLE organisation_organisation_2 RENAME TO organisation_organisation;

CREATE INDEX IF NOT EXISTS "organisation_organisation_created_by_id_38a608bc" ON "organisation_organisation" ("created_by_id");
CREATE INDEX IF NOT EXISTS "organisation_organisation_deleted_by_id_110093a5" ON "organisation_organisation" ("deleted_by_id");
CREATE INDEX IF NOT EXISTS "organisation_organisation_modified_by_id_0fb64673" ON "organisation_organisation" ("modified_by_id");


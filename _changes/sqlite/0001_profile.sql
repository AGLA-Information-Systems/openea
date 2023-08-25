CREATE TABLE "organisation_profile_2" ("id" char(32) NOT NULL PRIMARY KEY, "role" varchar(1024) NOT NULL, "phone" varchar(1024) NOT NULL, "address" varchar(1024) NOT NULL, "description" text NULL, "is_active" bool NOT NULL, "created_at" datetime NULL, "modified_at" datetime NULL, "deleted_at" datetime NULL, "created_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "deleted_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "modified_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "organisation_id" char(32) NULL REFERENCES "organisation_organisation" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO organisation_profile_2 SELECT * FROM organisation_profile;
DROP TABLE organisation_profile;
ALTER TABLE organisation_profile_2 RENAME TO organisation_profile;

CREATE INDEX IF NOT EXISTS "organisation_profile_created_by_id_c57d6e80" ON "organisation_profile" ("created_by_id");
CREATE INDEX IF NOT EXISTS "organisation_profile_deleted_by_id_57ca8e99" ON "organisation_profile" ("deleted_by_id");
CREATE INDEX IF NOT EXISTS "organisation_profile_modified_by_id_53e47efd" ON "organisation_profile" ("modified_by_id");
CREATE INDEX IF NOT EXISTS "organisation_profile_organisation_id_5b40cbea" ON "organisation_profile" ("organisation_id");
CREATE INDEX IF NOT EXISTS "organisation_profile_user_id_2c8fa866" ON "organisation_profile" ("user_id");

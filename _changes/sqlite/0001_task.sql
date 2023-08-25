CREATE TABLE "organisation_task_2" ("id" char(32) NOT NULL PRIMARY KEY, "name" varchar(1024) NOT NULL, "description" text NULL, "attachment" varchar(100) NULL, "type" varchar(10) NOT NULL, "status" varchar(10) NOT NULL, "config" text NULL, "error" text NULL, "started_at" datetime NULL, "ended_at" datetime NULL, "created_at" datetime NULL, "modified_at" datetime NULL, "deleted_at" datetime NULL, "created_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "deleted_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "modified_by_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED, "organisation_id" char(32) NULL REFERENCES "organisation_organisation" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
INSERT INTO organisation_task_2 SELECT * FROM organisation_task;
DROP TABLE organisation_task;
ALTER TABLE organisation_task_2 RENAME TO organisation_task;

CREATE INDEX IF NOT EXISTS "organisation_task_created_by_id_c18f720f" ON "organisation_task" ("created_by_id");
CREATE INDEX IF NOT EXISTS "organisation_task_deleted_by_id_e140ba91" ON "organisation_task" ("deleted_by_id");
CREATE INDEX IF NOT EXISTS "organisation_task_modified_by_id_70d1ccc7" ON "organisation_task" ("modified_by_id");
CREATE INDEX IF NOT EXISTS "organisation_task_organisation_id_7a364aca" ON "organisation_task" ("organisation_id");
CREATE INDEX IF NOT EXISTS "organisation_task_user_id_25b04341" ON "organisation_task" ("user_id");

DROP TABLE IF EXISTS "config";
CREATE TABLE "public"."config" (
    "id" BIGSERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "value" TEXT default NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY ("id")
);
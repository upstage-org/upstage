DROP TABLE IF EXISTS "asset_type";
CREATE TABLE "public"."asset_type" (
    "id" BIGSERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT default NULL,
    "file_location" TEXT NOT NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY ("id")
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "asset";
CREATE TABLE "public"."asset" (
    "id" BIGSERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "asset_type_id" integer NOT NULL,
    "owner_id" integer NOT NULL,
    "description" TEXT default NULL,
    "file_location" TEXT NOT NULL,
    "copyright_level" integer NOT NULL default 0,
    "created_on" timestamp DEFAULT (now() at time zone 'utc'),
    "updated_on" timestamp DEFAULT (now() at time zone 'utc'),
    "size" BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY ("id"),
    FOREIGN KEY (asset_type_id) REFERENCES asset_type(id),
    FOREIGN KEY (owner_id) REFERENCES upstage_user(id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "stage";
CREATE TABLE "public"."stage" (
    "id" BIGSERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT default NULL,
    "owner_id" integer NOT NULL,
    "file_location" character varying NOT NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc'),
    "last_access" timestamp without time zone,
    PRIMARY KEY ("id"),
    FOREIGN KEY (owner_id) REFERENCES upstage_user(id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "asset_attribute";
CREATE TABLE "public"."asset_attribute" (
    "id" BIGSERIAL NOT NULL,
    "asset_id" integer NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT default NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY ("id"),
    FOREIGN KEY (asset_id) REFERENCES asset(id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "stage_attribute";
CREATE TABLE "public"."stage_attribute" (
    "id" BIGSERIAL NOT NULL,
    "stage_id" integer NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT default NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY ("id"),
    FOREIGN KEY (stage_id) REFERENCES stage(id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "tag";
CREATE TABLE "public"."tag" (
    "id" BIGSERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "color" TEXT default NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY ("id")
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "media_tag";
CREATE TABLE "public"."media_tag" (
    "id" BIGSERIAL NOT NULL,
    "asset_id" integer NOT NULL,
    "tag_id" integer NOT NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY ("id"),
    FOREIGN KEY (asset_id) REFERENCES asset(id),
    FOREIGN KEY (tag_id) REFERENCES tag(id)
);

DROP TABLE IF EXISTS "asset_type";
CREATE TABLE "public"."asset_type" (
    "id" BIGSERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "file_location" TEXT NOT NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc')),
    PRIMARY KEY ("id")
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "asset";
CREATE TABLE "public"."asset" (
    "id" BIGSERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "asset_type_id" integer NOT NULL,
    "owner_id" integer NOT NULL,
    "description" text NOT NULL,
    "file_location" character varying NOT NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc')),
    PRIMARY KEY ("id"),
    FOREIGN KEY (asset_type_id) REFERENCES asset_type(id),
    FOREIGN KEY (owner_id) REFERENCES upstage_user(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "stage";
CREATE TABLE "public"."stage" (
    "id" BIGSERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "description" text NOT NULL,
    "owner_id" integer NOT NULL,
    "file_location" character varying NOT NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc')),
    PRIMARY KEY ("id"),
    FOREIGN KEY (owner_id) REFERENCES upstage_user(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "asset_license";
CREATE TABLE "public"."asset_license" (
    "id" BIGSERIAL NOT NULL,
    "asset_id" integer NOT NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc')),
    "expires_on" timestamp DEFAULT timezone('utc')) NOT NULL,
    "access_path" character varying unique NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY (asset_id) REFERENCES asset(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE
);

CREATE INDEX "asset_license_created_on" ON "public"."asset_license" USING btree ("created_on");
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "asset_attribute";
CREATE TABLE "public"."asset_attribute" (
    "id" BIGSERIAL NOT NULL,
    "asset_id" integer NOT NULL,
    "name" TEXT NOT NULL,
    "description" text NOT NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc')),
    PRIMARY KEY ("id"),
    FOREIGN KEY (asset_id) REFERENCES asset(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE
);
CREATE INDEX "asset_license_expires_on" ON "public"."asset_license" USING btree ("expires_on");
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "stage_attribute";
CREATE TABLE "public"."stage_attribute" (
    "id" BIGSERIAL NOT NULL,
    "stage_id" integer NOT NULL,
    "name" TEXT NOT NULL,
    "description" text NOT NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc')),
    PRIMARY KEY ("id"),
    FOREIGN KEY (stage_id) REFERENCES stage(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE
);

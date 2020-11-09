DROP TABLE IF EXISTS "assets";
DROP SEQUENCE IF EXISTS assets_id_seq;
CREATE SEQUENCE assets_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."assets" (
    "id" integer DEFAULT nextval('assets_id_seq') NOT NULL,
    "file_location" character varying NOT NULL,
    "owner_id" integer NOT NULL,
    "name" character(1) NOT NULL,
    "description" text NOT NULL,
    "created_on" timestamp DEFAULT timezone('utc')),
    CONSTRAINT "assets_id" PRIMARY KEY ("id"),
    CONSTRAINT "assets_owner_id_fkey" FOREIGN KEY (owner_id) REFERENCES upstage_user(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE
) WITH (oids = false);

DROP TABLE IF EXISTS "asset_licenses";
DROP SEQUENCE IF EXISTS asset_licenses_id_seq;
CREATE SEQUENCE asset_licenses_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."asset_licenses" (
    "id" bigint DEFAULT nextval('asset_licenses_id_seq') NOT NULL,
    "asset_id" bigint NOT NULL,
    "created_on" timestamp DEFAULT timezone('utc')) NOT NULL,
    "expires_on" timestamp DEFAULT timezone('utc')) NOT NULL,
    "access_path" character varying NOT NULL,
    CONSTRAINT "asset_licenses_access_path" UNIQUE ("access_path"),
    CONSTRAINT "asset_licenses_id" PRIMARY KEY ("id"),
    CONSTRAINT "asset_licenses_asset_id_fkey" FOREIGN KEY (asset_id) REFERENCES assets(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE
) WITH (oids = false);

CREATE INDEX "asset_licenses_created_on" ON "public"."asset_licenses" USING btree ("created_on");

CREATE INDEX "asset_licenses_expires_on" ON "public"."asset_licenses" USING btree ("expires_on");

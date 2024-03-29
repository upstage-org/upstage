-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "stage_license";
CREATE TABLE "public"."stage_license" (
    "id" BIGSERIAL NOT NULL,
    "stage_id" integer NOT NULL,
    "created_on" timestamp without time zone DEFAULT (now() at time zone 'utc'),
    "expires_on" timestamp without time zone NOT NULL,
    "access_path" character varying unique NOT NULL,
    PRIMARY KEY ("id"),
    FOREIGN KEY (stage_id) REFERENCES stage(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE
);

CREATE INDEX "stage_license_created_on" ON "public"."stage_license" USING btree ("created_on");
CREATE INDEX "stage_license_expires_on" ON "public"."stage_license" USING btree ("expires_on");
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "asset_license";
CREATE TABLE "public"."asset_license" (
    "id" BIGSERIAL NOT NULL,
    "asset_id" integer NOT NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc'),
    "level" integer NOT NULL,
    "permissions" TEXT,
    PRIMARY KEY ("id"),
    FOREIGN KEY (asset_id) REFERENCES asset(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE
);

CREATE INDEX "asset_license_created_on" ON "public"."asset_license" USING btree ("created_on");
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "asset_usage";
CREATE TABLE "public"."asset_usage" (
    "id" BIGSERIAL NOT NULL,
    "asset_id" integer NOT NULL,
    "user_id" integer NOT NULL,
    "approved" boolean NOT NULL DEFAULT false,
    "seen" boolean NOT NULL DEFAULT false,
    "note" TEXT,
    "created_on" timestamp DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY ("id"),
    FOREIGN KEY (asset_id) REFERENCES asset(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE,
    FOREIGN KEY (user_id) REFERENCES upstage_user(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE
);

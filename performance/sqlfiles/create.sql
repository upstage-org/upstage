DROP TABLE IF EXISTS "parent_stage";
CREATE TABLE "public"."parent_stage" (
    "id" BIGSERIAL NOT NULL,
    "stage_id" integer NOT NULL,
    "child_asset_id" integer NOT NULL,
    FOREIGN KEY (stage_id) REFERENCES stage(id),
    FOREIGN KEY (child_asset_id) REFERENCES asset(id),
    PRIMARY KEY ("id")
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "parent_asset";
CREATE TABLE "public"."parent_stage" (
    "id" BIGSERIAL NOT NULL,
    "asset_id" integer NOT NULL,
    "child_asset_id" integer NOT NULL,
    FOREIGN KEY (asset_id) REFERENCES asset(id),
    FOREIGN KEY (child_asset_id) REFERENCES asset(id),
    PRIMARY KEY ("id")
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "performance";
CREATE TABLE "public"."performance" (
    "id" BIGSERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT NOT NULL,
    "owner_id" integer NOT NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc')),
    "expires_on" timestamp DEFAULT null,
    PRIMARY KEY ("id")
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DROP TABLE IF EXISTS "scene";
CREATE TABLE "public"."scene" (
    "id" BIGSERIAL NOT NULL,
    "name" TEXT not null,
    "scene_order" integer not null default 0,
    "owner_id" integer not null default 0,
    "description" TEXT not null,
    "created_on" timestamp DEFAULT (now() at time zone 'utc')),
    "expires_on" timestamp DEFAULT null,
    "parent_stage_id" integer NOT NULL,
    "performance_id" integer NOT NULL,
    FOREIGN KEY (parent_stage_id) REFERENCES parent_stage(id),
    FOREIGN KEY (performnce_id) REFERENCES performance(id),
    FOREIGN KEY (owner_id) REFERENCES owner(id),
    PRIMARY KEY ("id")
);
CREATE INDEX "scene_scene_order_idx" ON "public"."scene" USING btree ("scene_order");

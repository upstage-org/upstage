DROP TABLE IF EXISTS "config";
CREATE TABLE "public"."config" (
    "id" BIGSERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "value" TEXT default NULL,
    "created_on" timestamp DEFAULT (now() at time zone 'utc'),
    PRIMARY KEY ("id")
);

-- Seed foyer config
INSERT INTO "config" ("name", "value") VALUES ('FOYER_TITLE', 'CYBERFORMANCE PLATFORM');
INSERT INTO "config" ("name", "value") VALUES ('FOYER_DESCRIPTION', 'UpStage is an online venue for live performance: remote performers collaborate in real time using digital media, and online audiences anywhere in the world join events by going to a web page, without having to download and install any additional software. UpStage is available free to anyone who would like to use it.');
INSERT INTO "config" ("name", "value") VALUES ('FOYER_MENU', 'About
> FAQ (https://upstage.org.nz/?page_id=115)
> Contact (https://upstage.org.nz/?page_id=5)
> Diversity & Inclusion (https://upstage.org.nz/?page_id=8361)
Festivals (https://upstage.org.nz/?page_id=1958)
Development (https://github.com/upstage-org/upstage/)
Donate (https://upstage.org.nz/?page_id=278)
Demo Stage (/demo)');
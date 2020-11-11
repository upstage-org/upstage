CREATE TABLE upstage_group (
        id BIGSERIAL NOT NULL,
        description TEXT not null default '',
        created_on timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE asset_group (
        id BIGSERIAL NOT NULL,
        description TEXT not null default '',
        group_id INTEGER NOT NULL DEFAULT 0,
        asset_id INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(group_id) REFERENCES upstage_group (id),
        FOREIGN KEY(asset_id) REFERENCES asset (id),
        created_on timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE stage_group (
        id BIGSERIAL NOT NULL,
        description TEXT not null default '',
        group_id INTEGER NOT NULL DEFAULT 0,
        stage_id INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(group_id) REFERENCES upstage_group (id),
        FOREIGN KEY(stage_id) REFERENCES stage (id),
        created_on timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE user_group (
        id BIGSERIAL NOT NULL,
        notes TEXT default null,
        group_id INTEGER NOT NULL DEFAULT 0,
        user_id INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(group_id) REFERENCES upstage_group (id),
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        created_on timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE user_asset (
        id BIGSERIAL NOT NULL,
        notes TEXT default null,
        asset_id INTEGER NOT NULL DEFAULT 0,
        user_id INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(asset_id) REFERENCES asset (id),
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        created_on timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE user_stage (
        id BIGSERIAL NOT NULL,
        notes TEXT default null,
        stage_id INTEGER NOT NULL DEFAULT 0,
        user_id INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(stage_id) REFERENCES stage (id),
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        created_on timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);

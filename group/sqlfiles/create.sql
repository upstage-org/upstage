CREATE TABLE public.upstage_group (
        id BIGSERIAL NOT NULL,
        description TEXT default null,
        created_on timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE public.asset_group (
        id BIGSERIAL NOT NULL,
        description TEXT default null,
        group_id INTEGER NOT NULL DEFAULT 0,
        asset_id INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(group_id) REFERENCES upstage_group (id),
        FOREIGN KEY(asset_id) REFERENCES asset (id),
        created_on timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE public.stage_group (
        id BIGSERIAL NOT NULL,
        description TEXT default null,
        group_id INTEGER NOT NULL DEFAULT 0,
        stage_id INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(group_id) REFERENCES upstage_group (id),
        FOREIGN KEY(stage_id) REFERENCES stage (id),
        created_on timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE public.user_group (
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
CREATE TABLE public.user_asset (
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
CREATE TABLE public.user_stage (
        id BIGSERIAL NOT NULL,
        notes TEXT default null,
        stage_id INTEGER NOT NULL DEFAULT 0,
        user_id INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(stage_id) REFERENCES stage (id),
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        created_on timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);

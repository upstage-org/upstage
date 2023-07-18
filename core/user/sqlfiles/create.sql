CREATE TABLE public.upstage_user (
        id BIGSERIAL NOT NULL,
        username TEXT unique not null,
        password TEXT not null,
        email TEXT unique default null,
        bin_name TEXT not null,
        role INTEGER not null default 0,
        first_name TEXT default null,
        last_name TEXT default null,
        display_name TEXT default null,
        active BOOLEAN not null default false,
        firebase_pushnot_id TEXT default null,
        created_on timestamp without time zone default (now() at time zone 'utc'),
        deactivated_on timestamp without time zone default null,
        upload_limit INTEGER,
        intro TEXT default null,
        can_send_email BOOLEAN default false,
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE public.user_pushnot (
        id BIGSERIAL NOT NULL,
        user_id INTEGER NOT NULL DEFAULT 0,
        push_notification TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        created_on timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE public.user_portal_config (
        id BIGSERIAL NOT NULL,
        user_id INTEGER UNIQUE NOT NULL DEFAULT 0,
        json_config TEXT NOT NULL DEFAULT '{"viewing_timezone":"US/Eastern"}',
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE public.admin_one_time_totp_qr_url (
        id BIGSERIAL NOT NULL,
        user_id INTEGER unique not null default 0,
        url TEXT NOT NULL,
        code TEXT NOT NULL,
        recorded_time timestamp without time zone default (now() at time zone 'utc'),
        active BOOLEAN not null default true,
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        PRIMARY KEY (id)
);

CREATE TABLE public.jwt_no_list (
        id BIGSERIAL NOT NULL,
        token TEXT unique not null,
        token_type TEXT not null,
        remove_after timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE public.user_session (
        id BIGSERIAL NOT NULL,
        user_id INTEGER not null default 0,
        access_token TEXT NOT NULL default '',
        refresh_token TEXT NOT NULL default '',
        recorded_time timestamp without time zone default (now() at time zone 'utc'),
        app_version TEXT NULL,
        app_os_type TEXT NULL,
        app_os_version TEXT NULL,
        app_device TEXT NULL,
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE public.google_profile (
        id BIGSERIAL NOT NULL,
        user_id INTEGER default null,
        google_id TEXT NOT NULL default '',
        google_phone TEXT default null,
        google_email TEXT default null,
        google_first_name TEXT default null,
        google_last_name TEXT default null,
        google_username TEXT default null,
        other_profile_json TEXT default null,
        received_datetime timestamp without time zone default (now() at time zone 'utc'),
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE public.facebook_profile (
        id BIGSERIAL NOT NULL,
        user_id INTEGER default null,
        facebook_id TEXT NOT NULL default '',
        facebook_phone TEXT default null,
        facebook_email TEXT default null,
        facebook_first_name TEXT default null,
        facebook_last_name TEXT default null,
        facebook_username TEXT default null,
        other_profile_json TEXT default null,
        received_datetime timestamp without time zone default (now() at time zone 'utc'),
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE public.apple_profile (
        id BIGSERIAL NOT NULL,
        user_id INTEGER default null,
        apple_id TEXT NOT NULL default '',
        apple_phone TEXT default null,
        apple_email TEXT default null,
        apple_first_name TEXT default null,
        apple_last_name TEXT default null,
        apple_username TEXT default null,
        other_profile_json TEXT default null,
        received_datetime timestamp without time zone default (now() at time zone 'utc'),
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        PRIMARY KEY (id)
);


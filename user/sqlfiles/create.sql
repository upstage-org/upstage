CREATE TABLE upstage_user (
        id SERIAL NOT NULL,
        username TEXT unique not null default '',
        password TEXT not null default '',
        email TEXT unique not null default '',
        bin_name TEXT not null default '',
        role INTEGER not null default 0,
        first_name TEXT default null,
        last_name TEXT default null,
        display_name TEXT default null,
        phone TEXT not null default '',
        active BOOLEAN not null default false,
        validated_via_portal BOOLEAN not null default false,
        ok_to_sms BOOLEAN not null default true,
        agreed_to_terms BOOLEAN not null default false,
        firebase_pushnot_id TEXT default null,
        created_on timestamp without time zone default (now() at time zone 'utc'),
        deactivated_on timestamp without time zone default null,
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE user_pushnot (
        id SERIAL NOT NULL,
        user_id INTEGER NOT NULL DEFAULT 0,
        push_notification TEXT NOT NULL DEFAULT '',
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        created_on timestamp without time zone default (now() at time zone 'utc'),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE user_portal_config (
        id SERIAL NOT NULL,
        user_id INTEGER UNIQUE NOT NULL DEFAULT 0,
        json_config TEXT NOT NULL DEFAULT '{"viewing_timezone":"US/Eastern"}',
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE nonuser_inquiry (
        id SERIAL NOT NULL,
        phone_number TEXT NOT NULL DEFAULT '',
        access_code TEXT NOT NULL DEFAULT '',
        verified BOOLEAN NOT NULL DEFAULT false,
        created_on timestamp without time zone default (now() at time zone 'utc'),
        first_name TEXT not null default '',
        last_name TEXT not null default '',
        email TEXT not null default '',
        full_address TEXT not null default '',
        found_match TEXT default null,
        PRIMARY KEY (id)
);
-- ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CREATE TABLE admin_one_time_totp_qr_url (
        id SERIAL NOT NULL,
        user_id INTEGER unique not null default 0,
        url TEXT NOT NULL default '',
        code TEXT NOT NULL default '',
        recorded_time timestamp without time zone default (now() at time zone 'utc'),
        active BOOLEAN not null default true,
        FOREIGN KEY(user_id) REFERENCES upstage_user (id),
        PRIMARY KEY (id)
);

DROP TABLE IF EXISTS "connection_stats";
DROP SEQUENCE IF EXISTS connection_stats_id_seq;
CREATE SEQUENCE connection_stats_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

create table connection_stats
(
	id serial
		constraint connection_stats_pk
			primary key,
	connected_id varchar,
	mqtt_timestamp timestamp,
	topic varchar,
	payload json,
	created timestamp
);

create index connection_stats_connected_id_index
	on connection_stats (connected_id);

create index connection_stats_created_index
	on connection_stats (created);


DROP TABLE IF EXISTS "receive_stats";
DROP SEQUENCE IF EXISTS receive_stats_id_seq;
CREATE SEQUENCE receive_stats_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

create table receive_stats
(
	id serial
		constraint receive_stats_pk
			primary key,
	received_id varchar,
	mqtt_timestamp timestamp,
	topic varchar,
	payload json,
	created timestamp
);

create index receive_stats_created_index
	on receive_stats (created);

create index receive_stats_received_id_index
	on receive_stats (received_id);


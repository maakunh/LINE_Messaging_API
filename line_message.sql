BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "line_message" (
	"update_flg"	TEXT,
	"send_message"	TEXT,
	"request_datetime"	TEXT,
	"send_datetime"	TEXT,
	"number"	INTEGER,
	"application"	TEXT
);
CREATE TABLE IF NOT EXISTS "line_flg" (
	"no"	INTEGER,
	"on"	INTEGER,
	"off"	INTEGER,
	"ignore"	INTEGER
);
CREATE TABLE IF NOT EXISTS "line_secret" (
	"application"	TEXT NOT NULL,
	"CHANNEL_ACCESS_TOKEN"	TEXT NOT NULL,
	"USER_ID"	TEXT NOT NULL,
	"enable"	INTEGER,
	PRIMARY KEY("application")
);
COMMIT;

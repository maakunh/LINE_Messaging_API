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

INSERT INTO "line_message" VALUES ('9','test','1970/01/01 00:00:00','1970/01/01 00:00:00',0,'TESTApp');
INSERT INTO "line_flg" VALUES (1,2,9,99);
INSERT INTO "line_secret" VALUES ('TESTApp','YourChannelAccessToken','YourUserId','1');

COMMIT;

BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "line_message" (
	"update_flg"	TEXT,
	"send_message"	TEXT,
	"request_datetime"	TEXT,
	"send_datetime"	TEXT,
	"number"	INTEGER,
	"application"	TEXT
);
INSERT INTO "line_message" VALUES ('9','test','1970/01/01 00:00:00','1970/01/01 00:00:00',0,'TESTApp');
INSERT INTO "line_message" VALUES ('9','test','2021/08/30 12:06:59','2021/08/30 12:06:59',1,'TESTApp');
COMMIT;

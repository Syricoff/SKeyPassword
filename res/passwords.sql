BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Types" (
	"id"	integer,
	"type_name"	string,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Passwords" (
	"id"	INTEGER,
	"app_name"	string NOT NULL,
	"login"	string NOT NULL,
	"password"	varchar NOT NULL,
	"type_app"	integer,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;

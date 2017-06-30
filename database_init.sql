CREATE TABLE IF NOT EXISTS hue_colors("id" integer PRIMARY_KEY, "name" text
 NOT NULL, "on" integer NOT NULL, "brightness" integer NOT NULL, "x" float,
 "y" float, "saturation" integer, "group" text);

CREATE TABLE IF NOT EXISTS pins("id" integer PRIMARY_KEY, "name" text NOT
NULL, "on" integer NOT NULL, "group" text);

DELETE FROM hue_colors;
DELETE FROM pins;

INSERT INTO pins("id", "name", "on", "group") VALUES (22, "michael_lamp", 0, "michael_room");

INSERT INTO hue_colors("id", "name", "on", "brightness", "x", "y",
"saturation", "group") VALUES (20, "michael_main_0", 0, 0, 0, 0, 0, "michael_room");

INSERT INTO hue_colors("id", "name", "on", "brightness", "x", "y",
"saturation", "group") VALUES (22, "michael_main_1", 0, 0, 0, 0, 0, "michael_room");


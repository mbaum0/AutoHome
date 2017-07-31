CREATE TABLE IF NOT EXISTS hue_colors("id" integer PRIMARY_KEY, "name" text
 NOT NULL, "on" integer NOT NULL, "brightness" integer NOT NULL, "x" float,
 "y" float, "saturation" integer, "group" text);

CREATE TABLE IF NOT EXISTS pins("id" integer PRIMARY_KEY, "name" text NOT
NULL, "on" integer NOT NULL, "group" text);

CREATE TABLE IF NOT EXISTS fans("id" integer PRIMARY_KEY, "name" text NOT NULL, "url" text NOT NULL,
 "speed" integer NOT NULL);

DELETE FROM hue_colors;
DELETE FROM pins;
DELETE FROM fans;

INSERT INTO pins("id", "name", "on", "group") VALUES (27, "michael_lamp", 0, "michael_room");

INSERT INTO hue_colors("id", "name", "on", "brightness", "x", "y",
"saturation", "group") VALUES (20, "michael_main_0", 0, 0, 0, 0, 0, "michael_room");

INSERT INTO hue_colors("id", "name", "on", "brightness", "x", "y",
"saturation", "group") VALUES (22, "michael_main_1", 0, 0, 0, 0, 0, "michael_room");

INSERT INTO fans("id", "name", "url", "speed") VALUES (0, "room_fan", "http://192.168.0.15/fan/speed/%d", 0);


PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
ANALYZE sqlite_master;
CREATE TABLE staffs( id INTEGER NOT NULL, name TEXT NOT NULL, gender TEXT NOT NULL, address TEXT NOT NULL, state TEXT NOT NULL, lga TEXT NOT NULL, dob DATE NOT NULL, phone TEXT NOT NULL, email TEXT, doe DATE NOT NULL, designation TEXT NOT NULL, level TEXT NOT NULL, PRIMARY KEY(id));
CREATE TABLE activity (id INTEGER, staff_id INTEGER NOT NULL, short_desc TEXT NOT NULL, full_desc TEXT NOT NULL, date_added DATE, PRIMARY KEY(id));
COMMIT;

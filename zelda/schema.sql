DROP TABLE IF EXISTS notes;


CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL
);
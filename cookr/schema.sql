DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS recipe;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE recipe (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  image TEXT,
  imageType TEXT,
  saving_user INTEGER NOT NULL,
  FOREIGN KEY (saving_user) REFERENCES user (id)
);

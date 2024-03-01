DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_preference;
DROP TABLE IF EXISTS saved_recipe;
DROP TABLE IF EXISTS recipe;
DROP TABLE IF EXISTS ingredient;
DROP TABLE IF EXISTS macro_info;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE user_preference (
  sweetness INTEGER NOT NULL,
  saltiness INTEGER NOT NULL,
  sourness INTEGER NOT NULL,
  bitterness INTEGER NOT NULL,
  savoriness INTEGER NOT NULL,
  fattiness INTEGER NOT NULL,
  spiciness INTEGER NOT NULL,
  saving_user INTEGER NOT NULL,
  FOREIGN KEY (saving_user) REFERENCES user (id)
);

CREATE TABLE recipe (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  creationTime DATETIME NOT NULL,
  selfHref TEXT NOT NULL,
  image TEXT,
  url TEXT NOT NULL,
  title TEXT NOT NULL,
  calories FLOAT NOT NULL,
  totalWeight FLOAT NOT NULL,
  totalTime FLOAT NOT NULL
);

CREATE TABLE ingredient (
  name TEXT NOT NULL,
  recipe_id INTEGER NOT NULL,
  primary key (name, recipe_id),
  FOREIGN KEY (recipe_id) REFERENCES recipe (id)
);

CREATE TABLE saved_recipe (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  image TEXT,
  imageType TEXT,
  saving_user INTEGER NOT NULL,
  FOREIGN KEY (saving_user) REFERENCES user (id)
);

CREATE TABLE macro_info (
  userWeight INTEGER TEXT NOT NULL,
  userSex TEXT NOT NULL,
  userHeight TEXT NOT NULL,
  userAge INTEGER NOT NULL,
  userActivityLevel TEXT NOT NULL,
  userCalories INTEGER NOT NULL,
  userProtein INTEGER NOT NULL,
  userCarbs INTEGER NOT NULL,
  userFat INTEGER NOT NULL,
  saving_user INTEGER NOT NULL,
  FOREIGN KEY (saving_user) REFERENCES user (id)
);
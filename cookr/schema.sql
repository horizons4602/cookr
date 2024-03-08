DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_preference;
DROP TABLE IF EXISTS user_nutrition;
DROP TABLE IF EXISTS user_health;
DROP TABLE IF EXISTS saved_recipe;
DROP TABLE IF EXISTS recipe;
DROP TABLE IF EXISTS ingredient;

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

CREATE TABLE user_nutrition (
  enabled BOOLEAN NOT NULL,
  age INTEGER,
  height INTEGER,
  weight INTEGER,
  activity_level INTEGER,
  saving_user INTEGER NOT NULL,
  FOREIGN KEY (saving_user) REFERENCES user (id)
);

CREATE TABLE user_health (
  alcohol_cocktail BOOLEAN NOT NULL,
  alcohol_free BOOLEAN NOT NULL,
  celery_free BOOLEAN NOT NULL,
  crustacean_free BOOLEAN NOT NULL,
  dairy_free BOOLEAN NOT NULL,
  dash BOOLEAN NOT NULL,
  egg_free BOOLEAN NOT NULL,
  fish_free BOOLEAN NOT NULL,
  fodmap_free BOOLEAN NOT NULL,
  gluten_free BOOLEAN NOT NULL,
  immuno_supportive BOOLEAN NOT NULL,
  keto_friendly BOOLEAN NOT NULL,
  kidney_friendly BOOLEAN NOT NULL,
  kosher BOOLEAN NOT NULL,
  low_fat_abs BOOLEAN NOT NULL,
  low_potassium BOOLEAN NOT NULL,
  low_sugar BOOLEAN NOT NULL,
  lupine_free BOOLEAN NOT NULL,
  Mediterranean BOOLEAN NOT NULL,
  mollusk_free BOOLEAN NOT NULL,
  mustard_free BOOLEAN NOT NULL,
  no_oil_added BOOLEAN NOT NULL,
  paleo BOOLEAN NOT NULL,
  peanut_free BOOLEAN NOT NULL,
  pescatarian BOOLEAN NOT NULL,
  pork_free BOOLEAN NOT NULL,
  red_meat_free BOOLEAN NOT NULL,
  sesame_free BOOLEAN NOT NULL,
  shellfish_free BOOLEAN NOT NULL,
  soy_free BOOLEAN NOT NULL,
  sugar_conscious BOOLEAN NOT NULL,
  sulfite_free BOOLEAN NOT NULL,
  tree_nut_free BOOLEAN NOT NULL,
  vegan BOOLEAN NOT NULL,
  vegetarian BOOLEAN NOT NULL,
  wheat_free BOOLEAN NOT NULL,
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
  totalTime FLOAT NOT NULL,
  saving_user INTEGER NOT NULL,
  FOREIGN KEY (saving_user) REFERENCES user (id)
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
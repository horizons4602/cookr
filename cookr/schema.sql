DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_preference;
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

CREATE TABLE user_health (
  alcohol-cocktail BOOLEAN NOT NULL,
  alcohol-free BOOLEAN NOT NULL,
  celery-free BOOLEAN NOT NULL,
  crustacean-free BOOLEAN NOT NULL,
  dairy-free BOOLEAN NOT NULL,
  DASH BOOLEAN NOT NULL,
  egg-free BOOLEAN NOT NULL,
  fish-free BOOLEAN NOT NULL,
  fodmap-free BOOLEAN NOT NULL,
  gluten-free BOOLEAN NOT NULL,
  immuno-supportive BOOLEAN NOT NULL,
  keto-friendly BOOLEAN NOT NULL,
  kidney-friendly BOOLEAN NOT NULL,
  kosher BOOLEAN NOT NULL,
  low-fat-abs BOOLEAN NOT NULL,
  low-potassium BOOLEAN NOT NULL,
  low-sugar BOOLEAN NOT NULL,
  lupine-free BOOLEAN NOT NULL,
  Mediterranean BOOLEAN NOT NULL,
  mollusk-free BOOLEAN NOT NULL,
  mustard-free BOOLEAN NOT NULL,
  no-oil-added BOOLEAN NOT NULL,
  paleo BOOLEAN NOT NULL,
  peanut-free BOOLEAN NOT NULL,
  pescatarian BOOLEAN NOT NULL,
  pork-free BOOLEAN NOT NULL,
  red-meat-free BOOLEAN NOT NULL,
  sesame-free BOOLEAN NOT NULL,
  shellfish-free BOOLEAN NOT NULL,
  soy-free BOOLEAN NOT NULL,
  sugar-conscious BOOLEAN NOT NULL,
  sulfite-free BOOLEAN NOT NULL,
  tree-nut-free BOOLEAN NOT NULL,
  vegan BOOLEAN NOT NULL,
  vegetarian BOOLEAN NOT NULL,
  wheat-free BOOLEAN NOT NULL,
  saving_user INTEGER NOT NULL,
  FOREIGN KEY (saving_user) REFERENCES user (id)
)

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
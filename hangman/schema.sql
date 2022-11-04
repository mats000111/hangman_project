DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS games_played;
-- DROP TABLE IF EXISTS post;
-- DROP TABLE IF EXISTS games_won;
-- DROP TABLE IF EXISTS games_lost;

-- CREATE TABLE user (
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   username TEXT UNIQUE NOT NULL,
--   password TEXT NOT NULL
-- );

-- CREATE TABLE post(
--   id INTEGER PRIMARY KEY AUTOINCREMENT,
--   author_id INTEGER NOT NULL,
--   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
--   title TEXT NOT NULL,
--   body TEXT NOT NULL,
--   FOREIGN KEY (author_id) REFERENCES user (id)
-- );

CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE games_played (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    won BOOLEAN,
    lost BOOLEAN,
    easy BOOLEAN,
    medium BOOLEAN,
    hard BOOLEAN,
    multiplayer BOOLEAN,
    time_played DATETIME DEFAULT(datetime()),
    FOREIGN KEY (user_id) REFERENCES user (id)
);

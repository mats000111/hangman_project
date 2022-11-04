DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS games_played;

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

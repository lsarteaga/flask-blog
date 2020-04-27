DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS post_features;
DROP TABLE IF EXISTS commentary;
DROP TABLE IF EXISTS commentary_features;

CREATE TABLE user(
  id_user INTEGER PRIMARY KEY,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL
);

CREATE TABLE post(
  id_post INTEGER PRIMARY KEY,
  id_user INTEGER NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (id_user) REFERENCES user (id_user) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE post_features(
  id_post_feature INTEGER PRIMARY KEY,
  id_post INTEGER NOT NULL,
  id_user INTEGER NOT NULL,
  like_p INTEGER DEFAULT 0,
  dislike_p INTEGER DEFAULT 0,
  FOREIGN KEY (id_post) REFERENCES post (id_post) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE UNIQUE INDEX idx_post ON post_features (id_user);


CREATE TABLE commentary(
  id_commentary INTEGER PRIMARY KEY,
  id_post INTEGER NOT NULL,
  id_user INTEGER NOT NULL,
  contend TEXT NOT NULL,
  FOREIGN KEY (id_post) REFERENCES post (id_post) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (id_user) REFERENCES user (id_user) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE commentary_features(
  id_commentary_features INTEGER PRIMARY KEY,
  id_commentary INTEGER NOT NULL,
  id_user INTEGER NOT NULL,
  like_c INTEGER DEFAULT 0,
  dislike_c INTEGER DEFAULT 0,
  FOREIGN KEY (id_commentary) REFERENCES commentary (id_commentary) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE UNIQUE INDEX idx_comm ON commentary_features (id_user);

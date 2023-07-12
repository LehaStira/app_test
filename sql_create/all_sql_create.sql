
CREATE TABLE Users (
  user_id integer primary key,
  username VARCHAR unique,
  email varchar unique,
  created_on timestamp,
  last_login timestamp,
  password varchar
);

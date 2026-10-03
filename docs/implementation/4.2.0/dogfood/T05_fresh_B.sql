CREATE TABLE schema_meta (version INTEGER NOT NULL);
INSERT INTO schema_meta(version) VALUES (2);

CREATE TABLE accounts (
  id INTEGER PRIMARY KEY,
  owner TEXT NOT NULL,
  balance_cents INTEGER NOT NULL,
  status TEXT NOT NULL
);

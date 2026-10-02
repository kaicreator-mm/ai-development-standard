CREATE TABLE schema_meta (version INTEGER NOT NULL);
INSERT INTO schema_meta(version) VALUES (1);

CREATE TABLE accounts (
  id INTEGER PRIMARY KEY,
  owner TEXT NOT NULL,
  balance_cents INTEGER NOT NULL,
  legacy_status TEXT NOT NULL
);

INSERT INTO accounts(id, owner, balance_cents, legacy_status) VALUES
  (1, 'alpha', 1250, 'active'),
  (2, 'beta', 9900, 'hold');

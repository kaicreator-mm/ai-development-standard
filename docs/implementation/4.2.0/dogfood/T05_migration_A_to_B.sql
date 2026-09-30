CREATE TABLE accounts_v2 (
  id INTEGER PRIMARY KEY,
  owner TEXT NOT NULL,
  balance_cents INTEGER NOT NULL,
  status TEXT NOT NULL
);

INSERT INTO accounts_v2(id, owner, balance_cents, status)
SELECT id, owner, balance_cents, legacy_status FROM accounts;

DROP TABLE accounts;
ALTER TABLE accounts_v2 RENAME TO accounts;
UPDATE schema_meta SET version = 2;

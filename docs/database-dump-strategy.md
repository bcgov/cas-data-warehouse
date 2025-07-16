
### Arcane Magic

```bash
sed_pattern='/\(^CREATE\sTRIGGER\|^COMMENT\sON\sTRIGGER\|^GRANT\|^CREATE\sPOLICY\|^CREATE\sFUNCTION\|^COMMENT\sON\sFUNCTION\)/,/--/{/--/!d}';
```

That allows us to prune triggers, grants, policies and functions from a pg_dump output.

### Explanation

Multi-line matcher removing lines from the first match (CREATE TRIGGER, COMMENT ON TRIGGER, ...) until the second match "--".
The pattern works like this:

```bash
/<pattern1>/,/<pattern2>/{<do stuff>}
```

Where:
- `pattern1` matches lines starting with "CREATE TRIGGER", "COMMENT ON TRIGGER", "GRANT", "CREATE POLICY", "CREATE FUNCTION" and "COMMENT ON FUNCTION"
- `pattern2` matches lines containing "--" (start of next item in pg_dump output)
- `/--/!d` means "if line does not match `--`, execute `d` (delete)"

Result: If line matches pattern1, delete until a pattern2 match.

### Usage

`pg_restore` needs the output of `pg_dump --format=custom` to run, which doesn't lend itself for manual processing with our `sed` command. To accomodate that and still use the `pg_restore` functions, we need to add a few steps:

- Create a temporary database `temp_db`
- Save edited dump into temporary database: `pg_dump -d <source db> ... | sed $sed_pattern | psql -d temp_db ...`
- Restore temporary database into the target with appropriate restore options: `pg_dump -d temp_db --format=custom | pg_restore --clean --if-exists --no-owner --role=... --no-privileges --single-transaction ...`
- Remove temporary database


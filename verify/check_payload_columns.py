#!/usr/bin/env python3
"""Verify every JS payload key in apply.html has a matching column in supabase-setup.sql."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APPLY = ROOT / "apply.html"
DDL = ROOT / "supabase-setup.sql"

apply_html = APPLY.read_text()
ddl = DDL.read_text()

# 1. Extract payload keys from the JSON.stringify body in submitToSupabase
body_match = re.search(r"const body = JSON\.stringify\(\{(.*?)\}\);", apply_html, re.S)
assert body_match, "could not find JSON.stringify body in apply.html"
keys = re.findall(r"^\s{4}([a-z_]+):", body_match.group(1), re.M)
print(f"Payload keys found in apply.html ({len(keys)}): {keys}")

# 2. Extract DDL columns from the CREATE TABLE block
create_match = re.search(r"CREATE TABLE IF NOT EXISTS public\.msp_applications \((.*?)\);", ddl, re.S)
assert create_match, "could not find CREATE TABLE block in supabase-setup.sql"
col_lines = [l.strip() for l in create_match.group(1).splitlines() if l.strip()]
cols = {}
for line in col_lines:
    m = re.match(r"([a-z_]+)\s+([A-Z]+(?:\([^)]*\))?)", line)
    if m:
        cols[m.group(1)] = m.group(2)
print(f"DDL columns found ({len(cols)}): {cols}")

# 3. Every payload key must have a column
missing = [k for k in keys if k not in cols]
print(f"\nMissing columns: {missing if missing else 'NONE'}")
if missing:
    sys.exit(1)

# 4. Type sanity: all payload values are strings -> TEXT columns
non_text = {k: t for k, t in cols.items() if k in keys and not t.startswith("TEXT")}
print(f"Non-TEXT columns for string payload keys: {non_text if non_text else 'NONE'}")
if non_text:
    sys.exit(1)

# 5. constraint_id present in both
print(f"constraint_id in payload: {'constraint_id' in keys}")
print(f"constraint_id in DDL: {'constraint_id' in cols}")

# 6. RLS checks
print(f"RLS enabled: {'ENABLE ROW LEVEL SECURITY' in ddl}")
print(f"anon INSERT policy: {'FOR INSERT TO anon' in ddl}")
print(f"anon SELECT policy present: {'FOR SELECT TO anon' in ddl}")

print("\nALL CHECKS PASSED")

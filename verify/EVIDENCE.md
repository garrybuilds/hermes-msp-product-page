# EVIDENCE — fix/msp-application-schema (Wave 1 / Branch 2)

## Finding
`apply.html` POSTs to `msp_applications` whose DDL existed in NO repo. Every insert failed while the UI showed "You're in 🎯" (false success). Form also lacked `constraint_id` and a double-submit guard.

## Changes
1. **`supabase-setup.sql` (new, repo root)** — `CREATE TABLE IF NOT EXISTS public.msp_applications` with a column for every payload key (TEXT for all string answers; `id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY`; `created_at TIMESTAMPTZ DEFAULT now()`; `constraint_id TEXT`). RLS enabled; anon INSERT `WITH CHECK (true)` only; no anon SELECT (block policies for select/update/delete).
2. **`apply.html`** — false-success removed: `showSuccess()` now renders a neutral "Submitting your application…" state; success ("✓ Application submitted") + Cal.com link reveal happen ONLY on confirmed insert (`r.ok`); explicit red error state on failure/network error. Double-submit guards: `isSubmitting` flag in `submitToSupabase()` + `goNext()` re-entry guard. `constraint_id` added to payload, derived from `leaking_workflow` (primary-pain question) via 6-vector taxonomy map (Lead response→demand, Scheduling→delivery, Follow-up→conversion, CRM & admin→support, Reviews & referrals→retention, Reporting→support, Other→demand; default demand).
3. **`index.html`** — no form/submit code found; not touched (per BRIEF task 5).

## Verification

### 1. Payload key ↔ DDL column check (verify/check_payload_columns.py)
```
$ python3 verify/check_payload_columns.py
Payload keys found in apply.html (16): ['name', 'email', 'company', 'website', 'team_size', 'industry', 'revenue', 'owner', 'bottleneck', 'leaking_workflow', 'urgency', 'budget', 'tier', 'case_study', 'call_time', 'constraint_id']
DDL columns found (18): {'id': 'BIGINT', 'created_at': 'TIMESTAMPTZ', 'name': 'TEXT', 'email': 'TEXT', 'company': 'TEXT', 'website': 'TEXT', 'team_size': 'TEXT', 'industry': 'TEXT', 'revenue': 'TEXT', 'owner': 'TEXT', 'bottleneck': 'TEXT', 'leaking_workflow': 'TEXT', 'urgency': 'TEXT', 'budget': 'TEXT', 'tier': 'TEXT', 'case_study': 'TEXT', 'call_time': 'TEXT', 'constraint_id': 'TEXT'}

Missing columns: NONE
Non-TEXT columns for string payload keys: NONE
constraint_id in payload: True
constraint_id in DDL: True
RLS enabled: True
anon INSERT policy: True
anon SELECT policy present: True

ALL CHECKS PASSED (exit 0)
```

### 2. No unconditional success path
```
$ grep -n "You're in\|Application submitted\|calLink.style.display" apply.html
549:  // (see submitToSupabase). No "You're in" here: that was a false success that
636:        statusEl.textContent = '✓ Application submitted';   <- inside r.ok branch only
639:        if (calLink) calLink.style.display = 'block';        <- inside r.ok branch only
```
Success text and Cal.com reveal are reachable only inside `if (r.ok)` (confirmed insert). Failure and catch paths set explicit red error text.

### 3. JS syntax
```
$ node --check <script extracted from apply.html>
(node --check: OK)
```

### 4. html-validate
```
$ npx html-validate apply.html
✖ 1 problem (1 error, 0 warnings)
  266:2  error  <button> is missing recommended "type" attribute  no-implicit-button-type
```
Single error is PRE-EXISTING (theme-toggle button, line 266 — verified by stashing changes and re-running; identical output). Not introduced by this fix.

### 5. Git diff scope
```
$ git status --short
 M apply.html
?? supabase-setup.sql
?? verify/
```
Only `apply.html` modified; `supabase-setup.sql` + `verify/` added. `index.html` untouched (no form/submit pattern present — verified by grep for supabase|fetch|form: only CSS/static content matches).

## Commit
`fix: create msp_applications DDL matching apply payload; false-success removed; constraint_id added`

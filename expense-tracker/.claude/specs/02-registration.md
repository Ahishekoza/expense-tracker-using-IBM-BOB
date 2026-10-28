# Spec: Registration

## Overview
Turn the static `/register` page into a working sign-up flow. A visitor submits their full name, email and password; the app validates the input, hashes the password with Werkzeug, stores a new row in the `users` table , shows the successfully signup message and  sends the visitor to the login page. This is the first write path into the data layer built in Step 1 and is the prerequisite for login and logout in the next step.

## Depends on
- Step 1 — Database setup (`users` table, `get_db()`, `init_db()`)

## Routes
- `GET /register` — render the registration form (already exists) — public
- `POST /register` — validate the form, create the user, redirect to `/login` on success; re-render the form with an error message on failure — public

Both methods are served by the existing `register` view function. Replace the stub in place; do not add a second route or rename the endpoint (`base.html` links to it with `url_for('register')`).

## Database changes
No database changes. The existing `users` table already has everything needed:
`id`, `name` (NOT NULL), `email` (UNIQUE, NOT NULL), `password_hash` (NOT NULL), `created_at` (defaults to `datetime('now')`).

## Templates
- **Create:** none
- **Modify:**
  - `templates/register.html`
    - change the form `action="/register"` to `action="{{ url_for('register') }}"`
    - repopulate the `name` and `email` inputs from the submitted values after a failed submit (`value="{{ name or '' }}"`, `value="{{ email or '' }}"`); never repopulate the password
    - add `minlength="8"` to the password input so the browser enforces the same rule as the server
    - keep the existing `{% if error %}` block, which already renders `.auth-error`

## Files to change
- `app.py` — import `request`, `redirect`, `url_for` from Flask, `generate_password_hash` from `werkzeug.security`, and `sqlite3`; implement the `GET`/`POST` handler for `register`
- `templates/register.html` — as described above

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only; never build SQL with string formatting
- Passwords hashed with werkzeug (`generate_password_hash`); never store or log the plain password
- Use CSS variables — never hardcode hex values. No new CSS is expected; reuse `.auth-error`, `.form-input`, `.btn-submit`
- All templates extend `base.html`
- Keep the route inside the existing "implemented routes" section of `app.py`, under the `# ---- #` banner
- Always link with `url_for('<endpoint>')`; page title stays `"Create account — Spendly"`
- Change the route decorator to `@app.route("/register", methods=["GET", "POST"])`
- Server-side validation (never rely on the browser alone):
  - `name`: strip whitespace, required
  - `email`: strip whitespace, lowercase, required, must contain `@` with text on both sides
  - `password`: required, minimum 8 characters
- Duplicate emails: check with a `SELECT` first, and also catch `sqlite3.IntegrityError` on the `INSERT` so a race cannot produce a 500. Show "An account with this email already exists."
- Validation failures re-render `register.html` with `error` set and return status `400`
- Always close the connection (`try`/`finally` or `with`)
- Success: `redirect(url_for('login'))`. Do not log the user in and do not add a session or `secret_key` here; that belongs to the login step
- Do not touch the other routes or the placeholder stubs

## Definition of done
- [ ] `GET /register` still renders the form with a 200 response
- [ ] Submitting a valid name, new email and password of 8+ characters redirects to `/login`
- [ ] The new row exists in `users` (check with `sqlite3 expense_tracker.db "SELECT id, name, email FROM users"`) and `password_hash` is a Werkzeug hash, not the plain password
- [ ] Registering the same email again, in any letter case (e.g. `A@x.com` after `a@x.com`), shows "An account with this email already exists." and creates no second row
- [ ] A password shorter than 8 characters is rejected with an error message (test by bypassing the browser `minlength`, e.g. with `curl`)
- [ ] An empty name, an empty email, or an email without `@` is rejected with an error message
- [ ] After a failed submit the name and email fields keep their values and the password field is empty
- [ ] The seeded demo user (`demo@spendly.com`) is untouched and a second seed run still adds no data
- [ ] The form's `action` is generated with `url_for('register')`, not hardcoded
- [ ] The app starts with `python app.py` on port 5001 with no errors

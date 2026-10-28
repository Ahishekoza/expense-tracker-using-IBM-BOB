# Spec: Login and Logout

## Overview
Turn the static `/login` page into a working sign-in flow and replace the `/logout` stub with a real sign-out. A visitor submits their email and password; the app looks the user up, verifies the password against the stored Werkzeug hash, and starts a Flask session. Logout clears that session. This is the first use of sessions in Spendly and is the prerequisite for every logged-in feature (profile, add/edit/delete expenses) in later steps. The shared nav in `base.html` also becomes session-aware so signed-in users see "Sign out" instead of "Sign in / Get started". Disable the access  to /login and /register URL , when the user is logged in . If loggedin user try to type the /login  or / register url in the browser it should always redirect to /profile page 

## Depends on
- Step 1 — Database setup (`users` table, `get_db()`)
- Step 2 — Registration (users with hashed passwords exist; `register` redirects to `login`)

## Routes
- `GET /login` — render the sign-in form (already exists). If a user is already logged in, redirect to `/profile` — public
- `POST /login` — validate the form, verify credentials, store the user in the session and redirect to `/profile` on success; re-render the form with an error message on failure — public
- `GET /logout` — clear the session and redirect to `/` (landing) — logged-in users in practice, but safe to call when logged out (just redirects)

`/login` is served by the existing `login` view function and `/logout` by the existing `logout` view function. Replace the stubs in place; do not add second routes or rename the endpoints (`base.html` and `register.html` link to them with `url_for(...)`).

## Database changes
No database changes. The existing `users` table already has everything needed: `id`, `name`, `email` (UNIQUE), `password_hash`.

## Templates
- **Create:** none
- **Modify:**
  - `templates/login.html`
    - change the form `action="/login"` to `action="{{ url_for('login') }}"`
    - repopulate the `email` input after a failed submit (`value="{{ email or '' }}"`); never repopulate the password
    - keep the existing `{% if error %}` block, which already renders `.auth-error`
  - `templates/base.html`
    - in `.nav-links`, branch on `session.get('user_id')`:
      - logged out: keep the existing "Sign in" and "Get started" links
      - logged in: show a "Sign out" link to `url_for('logout')` (reuse the existing `.nav-links a` styling; the `.nav-cta` class may be reused for emphasis)

## Files to change
- `app.py`
  - import `session` from Flask and `check_password_hash` from `werkzeug.security`
  - set `app.secret_key` (read from the `SECRET_KEY` environment variable, falling back to a clearly-labelled dev-only default)
  - implement the `GET`/`POST` handler for `login` inside the "implemented routes" section
  - move `logout` out of the "placeholder routes" section into the "implemented routes" section and implement it
- `templates/login.html` — as described above
- `templates/base.html` — as described above

## Files to create
None.

## New dependencies
No new dependencies. (`session` is part of Flask; `check_password_hash` is part of Werkzeug.)

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only; never build SQL with string formatting
- Passwords hashed with werkzeug — verify with `check_password_hash`; never compare plain text, store, or log the password
- Use CSS variables — never hardcode hex values. No new CSS is expected; reuse `.auth-error`, `.form-input`, `.btn-submit`
- All templates extend `base.html`
- Always link with `url_for('<endpoint>')`; page title stays `"Sign in — Spendly"`
- Change the login decorator to `@app.route("/login", methods=["GET", "POST"])`
- Keep the routes inside the existing "implemented routes" section of `app.py` under the `# ---- #` banner; do not touch the remaining placeholder stubs (`/profile`, `/expenses/*`)
- Server-side validation (never rely on the browser alone):
  - `email`: strip whitespace, lowercase, required
  - `password`: required (do not strip it)
- Look the user up by email with a parameterised `SELECT id, name, password_hash FROM users WHERE email = ?`
- Use one generic error for both an unknown email and a wrong password — "Invalid email or password." — so the form does not reveal which emails are registered
- Failed login re-renders `login.html` with `error` and the submitted `email`, and returns status `400` (match the registration route's convention)
- Always close the connection (`try`/`finally` or `with`)
- On success: `session.clear()` first (avoids session fixation), then store only `user_id` and `user_name` in the session, then `redirect(url_for('profile'))`
- Do not accept a `next` redirect parameter (avoids open-redirect issues)
- `SECRET_KEY` must never be hardcoded as the only option; the fallback is for local development only and must be commented as such
- Logout calls `session.clear()` and redirects to `url_for('landing')`
- Do not add a "remember me", password reset, or rate limiting; these are out of scope

## Definition of done
- [ ] `GET /login` renders the form with a 200 response when logged out
- [ ] Logging in as the seeded demo user (`demo@spendly.com` / `demo123`) redirects to `/profile` and the nav then shows "Sign out" instead of "Sign in" / "Get started"
- [ ] A user created through `/register` can log in with the email and password they registered with (email matching is case-insensitive, e.g. `A@X.com` works for `a@x.com`)
- [ ] A wrong password and an unknown email both show exactly "Invalid email or password." with status 400
- [ ] An empty email or empty password is rejected with an error message (test by bypassing the browser `required`, e.g. with `curl`)
- [ ] After a failed submit the email field keeps its value and the password field is empty
- [ ] While logged in, visiting `/login` redirects to `/profile` instead of showing the form
- [ ] Visiting `/logout` while logged in clears the session, redirects to `/`, and the nav shows "Sign in" / "Get started" again
- [ ] Visiting `/logout` while logged out does not error and redirects to `/`
- [ ] The session cookie contains no password or password hash (inspect the cookie / `session` contents: only `user_id` and `user_name`)
- [ ] The login form's `action` is generated with `url_for('login')`, not hardcoded
- [ ] The app starts with `python app.py` on port 5001 with no errors, and the other routes (`/`, `/register`, `/terms`, `/privacy`) still work

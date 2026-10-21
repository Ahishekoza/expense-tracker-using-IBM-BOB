# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Tutorial-style scaffold for "Spendly", a Flask expense-tracker app. Many routes are stubs labeled "Step N" for students to implement incrementally. Currency is rupees (copy says "Track every rupee"); keep UI text consistent.

## Architecture

```
expense-tracker/
├── app.py              # Flask app + all route handlers (implemented and placeholder)
├── database/
│   ├── __init__.py
│   └── db.py           # get_db() / init_db() / seed_db() — currently just a comment spec
├── templates/
│   ├── base.html        # shared layout: nav, footer, title/head/content/scripts blocks
│   ├── landing.html
│   ├── login.html
│   ├── register.html
│   ├── terms.html
│   └── privacy.html
├── static/
│   ├── css/
│   │   ├── style.css    # shared variables + base styles, loaded globally by base.html
│   │   └── landing.css  # landing-page-specific styles
│   └── js/
│       └── main.js      # shared JS, loaded globally by base.html
├── requirements.txt     # pinned deps: Flask 3.1.3, Werkzeug 3.1.6, pytest, pytest-flask
└── run.ps1              # Windows: activates venv and runs `python app.py`
```

- Single-file Flask app: everything lives in `app.py` (one `app` object, no blueprints/app factory yet).
- Implemented routes: `/`, `/register`, `/login`, `/terms`, `/privacy` (render templates only, no form handling).
- Placeholder routes in `app.py` (`/logout`, `/profile`, `/expenses/add`, `/expenses/<int:id>/edit|delete`) return plain strings referencing "Step N". Replace the stub in place rather than adding duplicate routes.
- `database/db.py` is currently only a comment spec. It must provide `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (`CREATE TABLE IF NOT EXISTS`), and `seed_db()` (dev sample data). The DB file is `expense_tracker.db` (gitignored).
- Templates extend `templates/base.html`, which defines the `title`, `head`, `content`, and `scripts` blocks and renders the shared nav/footer.

## Where things belong
- Page templates go in `templates/` and extend `base.html`'s blocks.
- Shared static assets: `static/css/style.css` (variables/base styles) and `static/js/main.js`, both loaded globally by `base.html`.
- Page-specific CSS gets its own file (e.g. `static/css/landing.css`); page-specific JS goes in that template's `scripts` block.
- Route handlers all live in `app.py`, split into sections by `# ---- #` banner comments (implemented routes vs. placeholder routes).

## Code Style
- Always link with `url_for('<endpoint>')`, where the endpoint is the view function name (e.g. `landing`, `login`, `register`). Renaming a view breaks `base.html` nav links.
- Page titles follow `"<Page> — Spendly"`.
- Keep the `# ---- #` banner-comment layout when adding routes to `app.py`.

## Tech Constraints
- Flask 3.1.3, Werkzeug 3.1.6, pinned in `requirements.txt`; use Werkzeug for password hashing.
- pytest + pytest-flask are available for testing, but no `tests/` dir or config exists yet.
- No lint/format/build tooling configured.

## Commands
- Create venv (first time only): `python -m venv venv`
- Activate venv: `.\venv\Scripts\Activate.ps1` (Windows PowerShell) / `source venv/bin/activate` (macOS/Linux)
- Install dependencies: `pip install -r requirements.txt`
- Run: `python app.py` (dev server on port **5001**, debug on; not Flask's default 5000). On Windows, `run.ps1` activates the venv and runs this.
- Test: `pytest` / single test: `pytest tests/test_file.py::test_name`

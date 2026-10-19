# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Commands
- Run: `python app.py` (dev server on port **5001**, debug on; not Flask's default 5000)
- Test: `pytest` / single test: `pytest tests/test_file.py::test_name` (pytest + pytest-flask are in `requirements.txt`, but no `tests/` dir or config exists yet)
- No lint/format/build tooling configured.

## Project state (tutorial-style scaffold, "Spendly")
- Flask app; everything is in `app.py` (single `app` object, no blueprints/app factory yet). Currently-implemented routes: `/`, `/register`, `/login` (render templates only, no form handling).
- Placeholder routes in `app.py` (`/logout`, `/profile`, `/expenses/add`, `/expenses/<int:id>/edit|delete`) return plain strings and reference "Step N". Replace the stub in place rather than adding duplicate routes.
- `database/db.py` is only a comment spec. It must provide `get_db()` (SQLite connection with `row_factory` and foreign keys enabled), `init_db()` (`CREATE TABLE IF NOT EXISTS`), and `seed_db()` (dev sample data). The DB file is `expense_tracker.db` (gitignored).
- Dependencies are pinned in `requirements.txt` (Flask 3.1.3, Werkzeug 3.1.6); use Werkzeug for password hashing.

## Conventions
- Templates extend `templates/base.html` and use its blocks: `title`, `head`, `content`, `scripts`. Titles follow `"<Page> — Spendly"`.
- Always link with `url_for('<endpoint>')`, where the endpoint is the view function name (e.g. `landing`, `login`, `register`). Renaming a view breaks `base.html` nav links.
- Static assets: `static/css/style.css` and `static/js/main.js` are loaded globally by `base.html`. Put page-specific JS in the `scripts` block.
- Currency is rupees (copy says "Track every rupee"); keep UI text consistent.
- Route sections in `app.py` are separated by `# ---- #` banner comments; keep that layout.

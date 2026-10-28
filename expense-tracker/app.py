import os
import sqlite3

from flask import Flask, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)
# Set SECRET_KEY in the environment for any real deployment. The fallback is a
# development-only value so the app runs locally; never rely on it in production.
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-insecure-key-change-me")

with app.app_context():
    init_db()
    seed_db()


AUTH_PAGE_ENDPOINTS = {"login", "register"}


@app.before_request
def redirect_logged_in_from_auth_pages():
    # A signed-in user can never reach the sign-in or sign-up pages, even by
    # typing the URL; they always land on their profile instead.
    if request.endpoint in AUTH_PAGE_ENDPOINTS and session.get("user_id"):
        return redirect(url_for("profile"))


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


MIN_PASSWORD_LENGTH = 8
DUPLICATE_EMAIL_ERROR = "An account with this email already exists."


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    

    def reject(message):
        # Re-render with the submitted name/email; the password is never echoed back.
        return render_template("register.html", error=message, name=name, email=email), 400

    if not name:
        return reject("Please enter your full name.")

    local_part, at_sign, domain = email.partition("@")
    if not (local_part and at_sign and domain):
        return reject("Please enter a valid email address.")

    if len(password) < MIN_PASSWORD_LENGTH:
        return reject(f"Password must be at least {MIN_PASSWORD_LENGTH} characters.")

    conn = get_db()
    try:
        if conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone():
            return reject(DUPLICATE_EMAIL_ERROR)

        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email, generate_password_hash(password)),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # Another request inserted the same email between our SELECT and INSERT.
        return reject(DUPLICATE_EMAIL_ERROR)
    finally:
        conn.close()

    return redirect(url_for("login"))


INVALID_LOGIN_ERROR = "Invalid email or password."


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    def reject(message):
        # Re-render with the submitted email; the password is never echoed back.
        return render_template("login.html", error=message, email=email), 400

    if not email or not password:
        return reject("Please enter your email and password.")

    conn = get_db()
    try:
        user = conn.execute(
            "SELECT id, name, password_hash FROM users WHERE email = ?",
            (email,),
        ).fetchone()
    finally:
        conn.close()

    # One generic message for unknown email and wrong password so the form
    # does not reveal which emails are registered.
    if user is None or not check_password_hash(user["password_hash"], password):
        return reject(INVALID_LOGIN_ERROR)

    session.clear()  # drop any pre-login session data (session fixation)
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("profile"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)

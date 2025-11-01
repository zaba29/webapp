import json
import os
from pathlib import Path
from typing import Dict

from flask import Flask, render_template, request, redirect, url_for, session, flash

BASE_DIR = Path(__file__).parent
CREDENTIALS_FILE = BASE_DIR / "data" / "credentials.json"


def load_credentials() -> Dict[str, str]:
    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError("Credentials file not found.")
    with CREDENTIALS_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_credentials(login: str, password: str) -> None:
    credentials = {"login": login, "password": password}
    with CREDENTIALS_FILE.open("w", encoding="utf-8") as file:
        json.dump(credentials, file, indent=2)


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "change-me")

    @app.route("/", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user_login = request.form.get("login", "").strip()
            password = request.form.get("password", "")

            credentials = load_credentials()
            if user_login == credentials.get("login") and password == credentials.get("password"):
                session["logged_in"] = True
                flash("Zalogowano pomyślnie.", "success")
                return redirect(url_for("admin"))

            flash("Niepoprawny login lub hasło.", "error")

        return render_template("login.html")

    def login_required(func):
        from functools import wraps

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not session.get("logged_in"):
                flash("Musisz się zalogować.", "error")
                return redirect(url_for("login"))
            return func(*args, **kwargs)

        return wrapper

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Wylogowano.", "info")
        return redirect(url_for("login"))

    @app.route("/admin", methods=["GET", "POST"])
    @login_required
    def admin():
        credentials = load_credentials()

        if request.method == "POST":
            new_login = request.form.get("new_login", "").strip()
            new_password = request.form.get("new_password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not new_login or not new_password:
                flash("Login i hasło nie mogą być puste.", "error")
            elif new_password != confirm_password:
                flash("Hasła muszą być takie same.", "error")
            else:
                save_credentials(new_login, new_password)
                flash("Dane logowania zostały zaktualizowane.", "success")
                return redirect(url_for("admin"))

        return render_template("admin.html", credentials=credentials)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)

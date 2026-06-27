"""Authentication routes."""

from flask import Blueprint, redirect, render_template, request, session, url_for

from database.user_store import authenticate_user, create_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Create a new user account."""
    if request.method == "GET":
        return render_template("register.html")

    name = request.form["username"]
    email = request.form["email"]
    mobile = request.form.get("mobile", "")
    password = request.form["password"]

    success, error_message = create_user(name, email, password, mobile)
    if not success:
        return render_template("register.html", error=error_message)

    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Authenticate a user and start a session."""
    if request.method == "GET":
        return render_template("login.html")

    identifier = request.form["identifier"]
    password = request.form["password"]
    remember_me = request.form.get("remember") == "on"

    user = authenticate_user(identifier, password)
    if not user:
        return render_template("login.html", error="Invalid login credentials")

    session.permanent = remember_me
    session["user"] = user
    return redirect(url_for("pages.home"))


@auth_bp.route("/logout")
def logout():
    """Clear the current session."""
    session.clear()
    return redirect(url_for("auth.login"))

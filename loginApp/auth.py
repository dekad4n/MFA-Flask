import functools

from flask import g     # global variable context
from flask import redirect, render_template, request, session, url_for, flash, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from bson.objectid import ObjectId

from db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id") # pymongo object id that is given in login
    db = get_db()

    if user_id is None:
        g.user = None
    else:
        g.user = db["User"].find_one({
                '_id': ObjectId(user_id)
        })


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.
    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        recoveryPhrase = request.form["recoveryPhrase"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif not email:
            error = "Email is required."
        elif not recoveryPhrase:
            error = "Recovery phrase is required."

        if error is None:
            user = db["User"].find_one({
                'username': username
            })
            if user is not None:
                # The username was already taken.
                error = f"User {username} is already registered."
            else:
                user = db["User"].find_one({
                    'email': email
                })
                if user is not None:
                # The email was already taken.
                    error = f"Email {email} is already registered."
                else:
                    db['User'].insert_one({
                        'username': username,
                        'password': generate_password_hash(password),
                        'email': email,
                        'recoveryPhrase': generate_password_hash(recoveryPhrase)
                    })
                    # Success, go to the login page.
                    return redirect(url_for("auth.login"))
        flash(error)
    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db["User"].find_one({
            'username': username
        })

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["user_id"] = str(user["_id"]) # pymongo object id
            return redirect(url_for("home.dashboard"))

        flash(error)

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
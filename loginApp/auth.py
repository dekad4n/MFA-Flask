import functools

from flask import g     # global variable context
from flask import redirect, render_template, request, session, url_for, flash, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash
from bson.objectid import ObjectId

from db import get_db
import smtplib
import pyotp
import secrets
import base64
import os



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


def sendEmail(code,to):

    # server = session.get('server')
    # if server is None:
    print("here",code)
    server = smtplib.SMTP('smtp.office365.com', port=587)
    server.starttls()
    # Login to the server (optional)
    server.login(os.environ['SMTP_HOTMAIL'], os.environ['HOTMAIL_PASSWORD'])
    # session['server'] = server
    # Set the recipient and message
    to = to
    subject = 'Two-factor authentication code'
    body = f'Your code is: {code}'
    msg = f'Subject: {subject}\n\n{body}'

    # Send the email
    server.sendmail(os.environ['SMTP_HOTMAIL'], to, msg)
    server.quit()

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
            query = {'username': username}
            key = secrets.token_bytes(16)
            base32_key = base64.b32encode(key).decode('utf-8')
            print(base32_key)
            totp = pyotp.TOTP(base32_key)
            secret_key = totp.now()

            data = {'username': username, "MFA": base32_key}
            sendEmail(secret_key, user["email"])
            db["MFA"].find_one_and_update(
                query, {"$set": data}, upsert=True)
            session["username"] = username
            return redirect("/auth/verification")

        flash(error)

    return render_template("auth/login.html")


def verify_otp(secret_key, otp):
    totp = pyotp.TOTP(secret_key)
    return totp.verify(otp)


@bp.route("/verification", methods=("GET","POST"))
def verification():
    print(request.method)
    if request.method=="POST":
        username = session["username"]
        error = None
        db = get_db()
        code = request.form["code"]
        if code is None:
            error = "No code sent"
        if error is None:
            user = db["MFA"].find_one({
                'username': username
            })
            print(user["MFA"])
            if verify_otp(user["MFA"],code):
                user= db["User"].find_one({'username': username})
                session.clear()
                session["user_id"] = str(user["_id"])  # pymongo object id
                return redirect(url_for("home.dashboard"))
            else: 
                error = "Invalid"
        flash(error)
    return render_template("auth/verification.html")

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))


@bp.route("/recover", methods=["POST","GET"])
def recover():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        recoveryPhrase = request.form["recoveryPhrase"]
        db = get_db()
        error = None
        user = db["User"].find_one({
            'username': username
        })

        if user is None:
            error = "Incorrect username."
        if error is None:
            if check_password_hash(user["recoveryPhrase"], recoveryPhrase):
                key = secrets.token_bytes(16)
                base32_key = base64.b32encode(key).decode('utf-8')
                totp = pyotp.TOTP(base32_key)
                secret_key = totp.now()
                sendEmail(secret_key, user["email"])
                data = {'username': username, "RMFA": base32_key}
                db["RMFA"].find_one_and_update(
                    {'username': username}, {"$set": data}, upsert=True)
                session["username"] = username
                return redirect(url_for("auth.recover_verification"))
            else:
                error = "Incorrect recovery phrase."
        flash(error)
    return render_template("auth/recover.html")

@bp.route("/recover/verification", methods=("GET","POST"))
def recover_verification():
    print(request.method)
    if request.method == "POST":
        username = session["username"]
        code = request.form["code"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db["RMFA"].find_one({
            'username': username
        })
        if code is None:
            error = "No code sent"
        user = db["RMFA"].find_one({'username': username})
        if user is None:
            error = "Incorrect username."
        if error is None:
            if verify_otp(user["RMFA"], code):
                db["User"].update_one({'username': username}, {
                                      '$set': {'password': generate_password_hash(password)}})
                return redirect(url_for("auth.login"))
            else:
                error = "Invalid code."
        flash(error)
    return render_template("auth/recover_verification.html")








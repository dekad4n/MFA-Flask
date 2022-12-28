from flask import session
import os
from dotenv import load_dotenv
from flask import request, flash
from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="OUR VERY VERY SECRET KEY",
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    import db
    load_dotenv()
    with app.app_context():
        db.init_app(app)

    # # apply the blueprints to the app
    import auth, home
    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)

    limiter = Limiter(key_func=get_remote_address)
    limiter.init_app(app)

    @app.before_request
    def before_request():
        try:
            with limiter.limit("10/minute"):
                print("Request")
        except:
            error = None
            if request.endpoint == "auth.login":
                username= None
                try:
                    username = request.form["username"]
                    cdb = db.get_db()
                    user = cdb["User"].find_one({
                        'username': username
                    })
                    if user is not None:
                        error = "We sent you email, check " + user["email"]
                except:
                    pass
                
            elif request.endpoint == "auth.verification":
                
                if session["username"] != None:
                    username = session["username"]
                    cdb = db.get_db()
                    user = cdb["User"].find_one({
                        'username': username
                    })
                    if user is not None:
                        error = "We sent you email, check " + user["email"]
                    else:
                        error = "No such user with username"
                else:
                    pass
            elif request.endpoint == "auth.recover":
                try:
                    username = request.form["username"]
                    cdb = db.get_db()
                    user = cdb["User"].find_one({
                        'username': username
                    })
                    if user is not None:
                        error = "We sent you email, check " + user["email"]
                    else:
                        try:
                            recoveryPhrase = request.form["recoveryPhrase"]
                            user = cdb["User"].find_one(
                                {'recoveryPhrase': recoveryPhrase})
                            if user is not None:
                                error = "Your username is wrong, did you mean " + \
                                    user["username"]
                            else:
                                error = "No user with recovery phrase" + recoveryPhrase
                        except:
                            pass
                except:
                    pass
            flash(error)
            return render_template("error_429.html")


    @app.route("/", methods=(["GET"]))
    def index():
        return render_template("index.html")

    
    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8081)
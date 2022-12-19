import os

from flask import Flask, render_template


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
    with app.app_context():
        db.init_app(app)

    # apply the blueprints to the app
    import auth, home
    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)

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
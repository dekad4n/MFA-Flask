import pymongo
import logging
import click
from flask import g
import os

from werkzeug.security import generate_password_hash

logger = logging.getLogger('db')


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = pymongo.MongoClient(os.environ['MONGO_URL'])

    return g.db.loginApp



def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    ex_user = db.loginApp['User'].find_one({
        "username": "exUser"
    })
    if ex_user is None:
        logger.info("Example user is not in collection.")
        user = {
            "username": "exUser",
            "password": generate_password_hash("123456789"),
            "email": "exUser@gmail.com",
            "recoveryPhrase": generate_password_hash("annemin kizlik soyadi")
        }
        db.loginApp['User'].insert_one(user)
        logger.info("Initialized the database with example user:", user)

def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    init_db()

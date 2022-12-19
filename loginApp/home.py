from flask import g     # global variable context
from flask import render_template, Blueprint

from auth import login_required
bp = Blueprint("home", __name__, url_prefix="/home")



@bp.route("/", methods=(["GET"]))
@login_required
def dashboard():
    return render_template("home/home.html")
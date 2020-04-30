from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog',__name__,url_prefix='/blog')

@bp.route('/')
def main():
    return render_template('blog/main.html')

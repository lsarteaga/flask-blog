from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Optional


bp = Blueprint('blog',__name__,url_prefix='/blog')

@bp.route('/')
def main():
    db = get_db()
    posts = db.execute(
        'SELECT id_post, title, body, created, p.id_user, username'
        ' FROM post p JOIN user u ON p.id_user= u.id_user'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/main.html', posts=posts)

@bp.route('/create', methods=['GET','POST'])
def create():
    form =  CreateForm()
    if form.validate_on_submit():
        db = get_db()
        db.execute(
            'INSERT INTO post (id_user,title,body)'
            ' VALUES (?,?,?)',
            (g.user['id_user'], form.title.data, form.body.data)
        )
        db.commit()
        return redirect(url_for('blog.main'))
    return render_template('blog/create.html', form=form)

class CreateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Content', validators=[DataRequired()])

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
@login_required
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

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT id_post, title, body, created, p.id_user, username'
        ' FROM post p JOIN user u ON p.id_user = u.id_user'
        ' WHERE p.id_post = ?',(id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['id_user'] != g.user['id_user']:
        abort(403)

    return post


@bp.route('/<int:id>/edit', methods=['GET','POST'])
@login_required
def edit(id):
    post = get_post(id)
    form = CreateForm()
    if form.validate_on_submit():
        db = get_db()
        db.execute(
            'UPDATE post SET title = ?, body = ?'
            ' WHERE id_post = ?',(form.title.data, form.body.data, id)
        )
        db.commit()
        return redirect(url_for('blog.main'))

    form.title.data = post['title']
    form.body.data = post['body']

    return render_template('blog/edit.html', form=form, post=post)

@bp.route('<int:id>/delete')
def delete(id):
    db = get_db()
    db.execute(
        'DELETE FROM post WHERE id_post = ?',(id,)
    )
    db.commit()
    return redirect(url_for('blog.main'))

@bp.route('<int:id>/user')
@login_required
def user_post(id):
    db = get_db()
    error = None
    posts = db.execute(
        'SELECT id_post, title, body, created, p.id_user , username FROM post p JOIN user u ON'
        ' p.id_user = u.id_user WHERE p.id_user = ? ORDER BY created DESC',(id,)
    ).fetchall()

    return render_template('user/user_post.html', posts=posts)

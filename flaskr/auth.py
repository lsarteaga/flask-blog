import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
####
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Optional
####
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db



bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        db = get_db()
        error = None
        value = db.execute(
            'SELECT id_user FROM user WHERE username = ?',(form.username.data,)
        ).fetchone()
        if value is not None:
            error = 'Username {} is already in use, try another'.format(form.username.data)
            flash(error)
        else:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?,?)',
                (form.username.data, generate_password_hash(form.password.data))
            )
            db.commit()
            return redirect('/')

    return render_template('auth/register.html', form=form)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6,message='Password too short')], description = 'Password must at least 6 characters')
    confirm_pwd = PasswordField('Repeat Password',
        validators=[DataRequired(), EqualTo('password',message='Passwords must match')])

@bp.route('/login',methods=['GET','POST'])
def login():
    form = LogginForm()
    if form.validate_on_submit():
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',(form.username.data,)
        ).fetchone()

        if user is None:
            error = 'Username {} is not registered yet,'.format(form.username.data)
        elif not check_password_hash(user['password'], form.password.data):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['id_user'] = user['id_user']
            ## in development .....
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html', form=form)

class LogginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me', validators = [Optional()])

@bp.before_app_request
def load_logged_in_user():
    id_user = session.get('id_user')
    if id_user is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id_user = ?',(id_user,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

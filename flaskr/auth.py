import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        db = get_db()
        error = None
        value = db.execute(
            'SELECT id_user FROM user WHERE username = ?', (username,)
        ).fetchone()
        if value is not None:
            error = 'User {} already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?,?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('success'))
        flash(error)
    return render_template('auth/register.html', form=form)

class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        validators.DataRequired(),
        validators.Length(max=25, message=['Username too long'])])
    password = PasswordField('Password', [
         validators.DataRequired(),
         validators.Length(min=8, message=('Password must be at least 8 characters.')),
         validators.EqualTo('Confirm Password', message='Passwords must match')
         ])
    submit = SubmitField('Submit')

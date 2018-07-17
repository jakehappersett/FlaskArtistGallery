import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        error = None
        username = request.form['username']
        password = request.form['password']

        if username is None:
            error = 'Enter a username'
        elif not username == current_app.config('USERNAME'):
            error = 'Ask Jake for your username'

        if password is None:
            error = 'Enter a password'
        elif not password == current_app.config('PASSWORD'):
            error = 'Ask Jake for your password'

        if error is None:
            session.clear()
            session['admin'] = True
        return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    admin = session.get('admin')

    if admin is None:
        g.user = None
    elif admin:
        g.user = 'admin'


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

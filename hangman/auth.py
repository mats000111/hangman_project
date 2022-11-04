import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort, make_response
)
from werkzeug.security import check_password_hash, generate_password_hash

from hangman.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        db = get_db()
        error = None

        if not username:
            # error = 'Username is required.'
            return abort(400)
        elif not password:
            # error = 'Password is required.'
            return abort(400)

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                # error = f"User {username} is already registered."
                return abort(400)
            else:
                data = {'message': 'Done', 'code': 'SUCCESS'}
                return make_response(jsonify(data), 201)
                # redirect(url_for("auth.login"))

        # flash(error)

    return "Hello World!"
    # return
    # render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            # error = 'Incorrect username.'
            return abort(400)
        elif not check_password_hash(user['password'], password):
            # error = 'Incorrect password.'
            return abort(400)

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            # return redirect(url_for('index'))
            data = {'username': username, 'password': password}
            return make_response(jsonify(data), 201)

        # flash(error)
    return "Hello World!"
    # return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    # return redirect(url_for('index'))
    return make_response(201)


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))

#         return view(**kwargs)

#     return wrapped_view

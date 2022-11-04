from flask import (
    Blueprint, g, request, session, jsonify, abort, make_response
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
            return abort(400)
        elif not password:
            return abort(400)

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                return abort(400)
            else:
                data = {'message': 'Done', 'code': 'SUCCESS'}
                return make_response(jsonify(data), 201)

    return "Hello World!"


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
            return abort(400)
        elif not check_password_hash(user['password'], password):
            return abort(400)

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            data = {'message': 'Done', 'code': 'SUCCESS'}
            return make_response(jsonify(data), 201)

    return "Hello World!"


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
    return make_response(201)


#!/usr/bin/env python3
""" Flask App
"""
import flask
from auth import Auth

AUTH = Auth()


app = flask.Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
    """
    form = {"message": "Bienvenue"}

    return flask.jsonify(form)


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """ POST /users
    """
    email = flask.request.form.get("email")
    password = flask.request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return flask.jsonify({"email": email, "message": "user created"})
    except ValueError:
        return flask.jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /login
    """
    email = flask.request.form.get("email")
    password = flask.request.form.get("password")

    if not AUTH.valid_login(email, password):
        flask.abort(401)

    try:
        session_id = AUTH.create_session(email)
        response = flask.jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    except Exception:
        flask.abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

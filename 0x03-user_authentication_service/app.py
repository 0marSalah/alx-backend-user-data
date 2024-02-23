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


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    Return:
        - Redirects to home route.
    """
    session_id = flask.request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        flask.abort(403)
    AUTH.destroy_session(user.id)
    return flask.redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Return:
        - JSON string of the user profile.
    """
    session_id = flask.request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        flask.abort(403)
    return flask.jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
    Return:
        - JSON string of the reset token.
    """
    email = flask.request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return flask.jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        flask.abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password
    Return:
        - JSON string of the reset token.
    """
    email = flask.request.form.get("email")
    reset_token = flask.request.form.get("reset_token")
    new_password = flask.request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return flask.jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        flask.abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

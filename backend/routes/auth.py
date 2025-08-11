from flask import Blueprint, request, jsonify
from backend.extensions import db, bcrypt
from flask_login import login_user, logout_user, login_required
from backend.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password_hash, password):
        login_user(user)                        #Stores user ID in session and marks user as authenticated.
        return jsonify({"message": "Login successful", "user_id": user.id})
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route("/logout", methods=["POST"])
@login_required                                 #before calling function, flask login checks if current_user autheticated or not (is_autheticated provided by user-mixin - inherited by user model)
def logout():
    logout_user()                               #flask-login removes _user_id from session -> session.pop('_user_id', None), and current_user.is_authenticated becomes false
    return jsonify({"message": "Logged out successfully"})

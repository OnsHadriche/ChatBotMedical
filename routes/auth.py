from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chatbot.index'))

    if request.method == "POST":
        
        data     = request.get_json()
        print("debug", data)
        email    = data.get('email', '').strip().lower()
        password = data.get('password', '')
        remember = data.get('remember', False)

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

        login_user(user, remember=remember)
        return jsonify({'success': True, 'message': 'Login successful',
                        'redirect': url_for('chatbot.index')})

    return render_template('login.html')


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('/'))

    if request.method == "POST":
        data       = request.get_json()
        print("recieve data", data)
        fullname   = data.get('fullname', '').strip()
        email      = data.get('email', '').strip().lower()
        phone      = data.get('phone', '').strip()
        password   = data.get('password', '')
        newsletter = data.get('newsletter', False)

        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 409

        new_user = User(
            fullname   = fullname,
            email      = email,
            phone      = phone or None,
            password   = generate_password_hash(password),
            newsletter = newsletter
        )
        print("new user", new_user)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Account created successfully',
                        'redirect': url_for('auth.login')})

    return render_template('register.html')


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route("/forgot-password")
def forgot_password():
    return render_template('forgot_password.html')
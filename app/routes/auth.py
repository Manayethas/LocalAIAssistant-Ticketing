from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required
from app import db
from app.models.user import User
from app.auth.ad_auth import authenticate_ad_user
from werkzeug.security import generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        auth_type = request.form.get('auth_type', 'local')  # Default to local auth
        
        if auth_type == 'ad':
            # Try AD authentication
            ad_user, error = authenticate_ad_user(username, password)
            if error:
                flash(f'AD Authentication failed: {error}', 'error')
                return redirect(url_for('auth.login'))
            
            # Check if user exists in local DB, create if not
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(
                    username=username,
                    email=f"{username}@{current_app.config['AD_DOMAIN']}",
                    is_technician=ad_user['is_technician']
                )
                # Set a random password since we'll use AD auth
                user.set_password('ad_auth_only')
                db.session.add(user)
                db.session.commit()
            
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            # Local authentication
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('main.index'))
            
            flash('Invalid username or password', 'error')
        
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('auth.register'))
            
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index')) 
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from src.models.models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
        
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False
        
        user = User.query.filter_by(email=email).first()
        
        # Check if user exists and password is correct
        if not user or not check_password_hash(user.password, password):
            flash("Please check your login details and try again.")
            return render_template("login.html")
            
        # If validation passes, log in the user
        login_user(user, remember=remember)
        
        # Redirect to the page the user was trying to access
        next_page = request.args.get("next")
        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("main.index")
            
        return redirect(next_page)
        
    return render_template("login.html")

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
        
    if request.method == "POST":
        # Handle form submission
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if user already exists
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash("Email address already exists")
            return redirect(url_for("auth.signup"))
        
        if username_exists:
            flash("Username already exists")
            return redirect(url_for("auth.signup"))

        # Create new user with password hash
        new_user = User(email=email, username=username, password=password)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.")
        return redirect(url_for("auth.login"))
    
    # GET request - show the signup form
    return render_template("signup.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@auth.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user) 
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from src.models.models import User, db
from urllib.parse import urlparse

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
        
    if request.method == "POST":
        login_id = request.form.get("email")  # This could be email or username
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False
        
        # Try to find user by email or username
        user = User.query.filter(
            (User.email == login_id) | (User.username == login_id)
        ).first()
        
        # Check if user exists and password is correct
        if not user or not user.check_password(password):
            flash("Please check your login details and try again.", "error")
            return render_template("login.html")
            
        # If validation passes, log in the user
        login_user(user, remember=remember)
        
        # Clear any error messages since login was successful
        session.pop('_flashes', None)
        
        # Redirect to the page the user was trying to access
        next_page = request.args.get("next")
        if not next_page or urlparse(next_page).netloc != "":
            next_page = url_for("main.index")
            
        return redirect(next_page)
        
    # Clear any old messages when showing the login form
    session.pop('_flashes', None)
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
            flash("Email address already exists", "error")
            return redirect(url_for("auth.signup"))
        
        if username_exists:
            flash("Username already exists", "error")
            return redirect(url_for("auth.signup"))

        # Create new user
        new_user = User(email=email, username=username, password=password)
        
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
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

@auth.route("/profile/update", methods=["POST"])
@login_required
def update_profile():
    if request.method == "POST":
        user = current_user
        
        # Get form data
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        
        # Update user information
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
            
        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
        except Exception:
            db.session.rollback()
            flash("An error occurred while updating your profile.", "error")
            
        return redirect(url_for("auth.profile"))

@auth.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        # Get form data
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        
        # Validate input
        if not current_password or not new_password or not confirm_password:
            flash("All fields are required", "error")
            return redirect(url_for("auth.change_password"))
            
        if new_password != confirm_password:
            flash("New passwords don't match", "error")
            return redirect(url_for("auth.change_password"))
            
        # Check if current password is correct
        if not current_user.check_password(current_password):
            flash("Current password is incorrect", "error")
            return redirect(url_for("auth.change_password"))
            
        # Update password
        current_user.set_password(new_password)
        
        try:
            db.session.commit()
            flash("Password changed successfully!", "success")
            return redirect(url_for("auth.profile"))
        except Exception:
            db.session.rollback()
            flash("An error occurred while changing your password.", "error")
            return redirect(url_for("auth.change_password"))
    
    # GET request - show the change password form
    return render_template("change_password.html") 
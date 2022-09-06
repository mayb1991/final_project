from flask import Blueprint, render_template, request, redirect, url_for, flash
from .forms import NewUserForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app.models import db, User


auth = Blueprint('auth', __name__, template_folder="authtemplates")


@auth.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = NewUserForm()
    if request.method == "POST":
        print("POST MADE")
        if form.validate():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            username = form.username.data
            password = form.password.data

            user = User(first_name, last_name, email, username, password)

            # adding users to db
            db.session.add(user)
            db.session.commit()

            flash("You are now created")
            return redirect(url_for('auth.login'))
        else:
            flash("You made a mistake somewhere in your form please try again")
    return render_template('signup.html', form=form)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()

            if user:
                if check_password_hash(user.password, password):
                    flash(f"Welcome back {username}", 'success')
                    login_user(user)
                    return redirect(url_for('home_page'))
                else:
                    flash("You enter the incorrect username or password please try again", 'danger')
            else: flash("User with that username does not exist.", 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    

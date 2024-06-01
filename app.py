import pymysql
from flask import Flask, flash, redirect, render_template, url_for
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_required, login_user, logout_user

from forms import LoginForm, PostForm, RegistrationForm
from models import db, login_manager
from models.models import Post, User

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
login_manager.login_view = "login"
pymysql.install_as_MySQLdb()


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/project")
def project():
    return render_template("project.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/board", methods=["GET", "POST"])
@login_required
def board():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("board"))
    posts = Post.query.all()
    return render_template("board.html", title="Board", form=form, posts=posts)


@app.route("/intro", methods=["GET"])
def intro():
    return render_template("intro.html")


@app.route("/error", methods=["GET"])
def error():
    return render_template("404.html")


if __name__ == "__main__":
    app.run(port=5000, debug=True)

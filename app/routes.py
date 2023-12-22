from app import app, db, bcrypt
from flask import render_template, url_for, flash, redirect
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post 
from flask_login import login_user

posts = [
    {
        'author': "Hamed Mani",
        'title': "blog post 1",
        'content': "First post content",
        'date': "April 20,2023"
    },
    {
        'author': "Hamza Mejri",
        'title': "blog post 2",
        'content': "Second post content",
        'date': "April 21,2023"
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data , email = form.email.data , password = hashed_password )
        db.session.add(user) 
        db.session.commit()
        flash('Welcome aboard ! You are now able to log in ','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form) 

@app.route('/login',  methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unseccessful, Please check email and password', 'danger')
    return render_template('login.html',title='Login', form=form) 

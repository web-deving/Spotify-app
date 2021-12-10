from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, MusicForm
from app.models import User, Song
from app.functions import *
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = MusicForm()
    user = User.query.filter_by(username=current_user.username).first()
    if request.method == 'POST':
        energy_v = request.form['energy']
        feeling_v = request.form['feeling']
        if form.submit1.data:
            #  use user songs
            recommend_specific(float(feeling_v),float(energy_v),1)
        elif form.submit2.data:
            #  use dataset
            name_,artist_,id = recommend_general(float(feeling_v),float(energy_v),1)
            link = "https://open.spotify.com/embed/track/" + str(id) + "?theme=0"
            song = Song(name=name_,artist=artist_,
                        link=link,energy=energy_v,valence=feeling_v, listener = user)
            db.session.add(song)
            db.session.commit()
            print(song)
            return render_template('songs.html', user=user)

    return render_template('index.html', title='Home', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/songs')
def songs():
    user = User.query.filter_by(username=current_user.username).first()
    return render_template('songs.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

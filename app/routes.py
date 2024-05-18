# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User
from urllib.parse import urlsplit
from datetime import datetime, timezone

menu = ["Микроблог", "Информация о сайте", "Обратная связь"]


@app.route('/')
@app.route('/index')
@login_required
def index():
    # user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'I am glad to see your posts here!'
        },
        {
            'author': {'username': 'Mindi'},
            'body': 'Wow! Hey there!'
        }
    ]
    return render_template('index.html', title='Home Page', posts=posts, menu=menu)
    # return render_template('index.html', title='Home Page', user=user, posts=posts, menu=menu)


@app.route("/about")
@login_required
def about():
    return render_template('about.html', title='About')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # проверяем если user уже вошел в систему, то перенаправляем на главную страницу
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # передаем форму Логина для заполнения
    form = LoginForm()
    # если user нажал submit подключаемся к БД и проверяем введенные данные с данными БД таблиц User
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        # если не введены данные или не проходит проверка пароля, то выдаем сообщение о неверных данных, введенных и
        # заново перенаправляем на заполнение формы
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # если проверка прошла, то сохраняем выводим сообщение и перенаправляем на запрашиваемую страницу до входа
        login_user(user, remember=form.remember_me.data)
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        # достаем запрашиваемую до входа страницу
        next_page = request.args.get('next')
        # если запрашиваемой страницы нет или адрес с доменом(netloc), то перенаправляем на корневую страницу (в случае
        # адреса с доменом перенаправление делаем в целях безопасности для исключения прохода по вредоносной ссылке
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        # return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

    # if form.validate_on_submit():
    #     flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))


@app.route('/logout')
def logout():
    # для выхода запускаем встроенную функцию выхода в Login
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # проверяем если user уже вошел в систему, то перенаправляем на главную страницу
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # передаем форму Регистрации для заполнения
    form = RegistrationForm()
    # если user нажал submit создаем экземпляр класса User, хэшируем пароль, добавляем запись в БД, поздравляем и
    # перенаправляем на страницу входа для ввода логина и пароля
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]

    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
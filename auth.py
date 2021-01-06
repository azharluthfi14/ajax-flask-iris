from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import db, User, Classification
from flask_login import login_user, login_required, current_user, logout_user
from PIL import Image
from .forms import register_account, login_account, update_account

auth = Blueprint('auth', __name__)


@auth.route("/register", methods=['GET', 'POST'])
def user_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = register_account()
    if form.validate_on_submit():
        user_exist = User.query.filter_by(email=form.email.data).first()
        if user_exist is None:
            user = User(username=form.username.data, first_name=form.first_name.data,
                        last_name=form.last_name.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(
                f'Account has been created for {form.username.data}.', 'success')
            return redirect(url_for('auth.login'))
    return render_template("register.html", form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = login_account()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash(f'Invalid username or password combination', 'danger')
    return render_template("signin.html", form=form)


@auth.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = update_account()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar_file = save_avatar(form.avatar.data)
            current_user.avatar = avatar_file
            current_user.username = form.username.data
            current_user.first_name = form.first_name.data
            current_user.last_name = form.last_name.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated.', 'success')
        return redirect(url_for('auth.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        avatar = url_for('static', filename='profile_img/' +
                         current_user.avatar)
    return render_template('account.html', avatar=avatar, form=form)


def save_avatar(form_avatar):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_avatar.filename)
    avatar_fn = random_hex + f_ext
    avatar_path = os.path.join(app.root_path, 'static/profile_img', avatar_fn)

    output_size = (125, 125)
    i = Image.open(form_avatar)
    i.thumbnail(output_size)
    i.save(avatar_path)

    return avatar_path


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been log out!', 'success')
    return redirect(url_for('auth.login'))

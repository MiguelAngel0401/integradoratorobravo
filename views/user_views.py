from flask import Blueprint, render_template, redirect, url_for, flash, abort, session, request

from models.users import User

from forms.user_forms import RegisterForm, LoginForm, ProfileForm

from utils.file_handler import save_image

user_views = Blueprint('user', __name__)

@user_views.route('/users/')
@user_views.route('/users/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.get_by_password(username, password)
        if not user:
            flash('Verifica tus Datos')
        else:
            session["user"]= user.username
            return redirect(url_for('home.home'))
    return render_template('users/login.html', form=form)


@user_views.route('/users/<int:page>/', methods=('GET',))
def users(page=1):
    if "user" in session:
        limit = 10
        users = User.get_all(limit=limit, page=page)
        total_users = User.count()
        pages = total_users // limit
        user = session.get("user")
        return render_template('users/users.html', users=users, pages=pages, user=user)
    return redirect(url_for('user.login'))

@user_views.route('/users/register/', methods=('GET', 'POST'))
def register():
    if "user" in session:
        form = RegisterForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data

            user = User(username, password, email)
            user.save()
            flash('Usario registrado con exito!')
            return redirect(url_for('user.logout'))
        return render_template('users/register.html', form=form)
    return redirect(url_for('user.login'))

@user_views.route('/users/logout/')
def logout():
    session.pop('user',None)
    return redirect(url_for('user.login'))

@user_views.route('/users/T&C Bar - Restaurante "El Toro Bravo: Food and Drinks"/')
def conditions():
    return render_template('home/conditions.html')


@user_views.route('/users/<int:id>/profile/', methods=('GET', 'POST'))
def profile(id):
    if "user" in session:
        form = ProfileForm()
        user = User.__get__(id)
        if not user:
            abort(404)
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            f = form.image.data
            if f:
                user.image = save_image(f, 'images/profiles', user.username)
            user.save()
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        image = user.image
        return render_template('users/profile.html', form=form, image=image)
    return redirect(url_for('user.login'))

@user_views.before_request
def antes_de_iniciar():
    ruta = request.path
    if 'user' not in session and ruta != "/users/" and ruta != "/users/logout/" and not ruta.startswith("/static") and ruta != "/users/login/":
        flash("Es necesario iniciar sesion.")
        return redirect(url_for('user.login'))
    

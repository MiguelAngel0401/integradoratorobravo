from flask import Blueprint, render_template, redirect, url_for, flash, request, session

from models.categories import Category 

from forms.category_forms import UpdateCategoryForm, CreateCategoryForm

category_views = Blueprint('category', __name__)

@category_views.route('/categories/')
def categories():
    if "user" in session:
        categories = Category.get_all()
        user = session.get("user")
        return render_template('categories/categories.html',
                            categories=categories, user=user)
    return redirect(url_for('user.login'))


@category_views.route('/categories/create/', methods=('GET', 'POST'))
def create_cat():
    if "user" in session:
        form = CreateCategoryForm()
        if form.validate_on_submit():
            category = form.category.data
            description = form.description.data
            cat = Category(category, description)
            cat.save()
            return redirect(url_for('category.categories'))
        return render_template('categories/create_cat.html', form=form)
    return redirect(url_for('user.login'))

@category_views.route('/categories/<int:id>/update/', methods=('GET', 'POST'))
def update_cat(id):
    if "user" in session:
        form = UpdateCategoryForm()
        cat = Category.get(id)
        if form.validate_on_submit():
            cat.category = form.category.data
            cat.description = form.description.data
            cat.save()
            return redirect(url_for('category.categories'))
        form.category.data = cat.category
        form.description.data = cat.description
        return render_template('categories/create_cat.html', form=form )
    return redirect(url_for('user.login'))

@category_views.route('/categories/<int:id>/delete/', methods=('POST',))
def delete_cat(id):
    if "user" in session:
        cat = Category.get(id)
        cat.delete()
        return redirect(url_for('category.categories'))
    return redirect(url_for('user.login'))

@category_views.before_request
def antes_de_iniciar():
    ruta = request.path
    if 'user' not in session and ruta != "/categories/" and ruta != "/categories/create/" and not ruta.startswith("/static"):
        flash("Es necesario iniciar sesion.")
        return redirect(url_for('user.login'))
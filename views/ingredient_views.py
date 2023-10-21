from flask import Blueprint, render_template, redirect, url_for, flash, request, session

from models.ingredients import Ingredient 

from forms.ingredient_forms import UpdateIngredientForm, CreateIngredientForm

from utils.file_handler import save_image

ingredient_views = Blueprint('ingredient', __name__)

@ingredient_views.route('/ingredients/')
def ingredients():
    if "user" in session:
        ingredients = Ingredient.get_all()
        user = session.get("user")
        return render_template('ingredients/ingredient.html',
                            ingredients=ingredients, user=user)
    return redirect(url_for('user.login'))

@ingredient_views.route('/ingredients/create/', methods=('GET', 'POST'))
def create_ingre():
    if "user" in session:
        form = CreateIngredientForm()
        if form.validate_on_submit():
            name = form.name.data
            marca = form.marca.data
            size = form.size.data
            stock = form.stock.data
            f = form.image.data
            image = ""
            if f:
                image = save_image(f, 'images/ingredients')
            ing = Ingredient(name=name, 
                            marca=marca,
                            size=size,
                            stock=stock,
                            image=image)
            ing.save()
            return redirect(url_for('ingredient.ingredients'))
        return render_template('ingredients/create_ingre.html', form=form)
    return redirect(url_for('user.login'))

@ingredient_views.route('/ingredients/<int:id>/update/', methods=('GET', 'POST'))
def update_ingre(id):
    if "user" in session:
        form = UpdateIngredientForm()
        ing = Ingredient.get(id)
        if form.validate_on_submit():
            ing.name = form.name.data
            ing.marca = form.marca.data
            ing.size = form.size.data
            ing.stock = form.stock.data
            f = form.image.data
            if f:
                image = save_image(f, 'images/ingredients')
                ing.image = image
            ing.save()
            return redirect(url_for('ingredient.ingredients'))
        form.name.data = ing.name
        form.marca.data = ing.marca
        form.size.data = ing.size
        form.stock.data = ing.stock
        image = ing.image
        return render_template('ingredients/create_ingre.html', form=form )
    return redirect(url_for('user.login'))

@ingredient_views.route('/ingredients/<int:id>/delete/', methods=['POST'])
def delete_ingre(id):
    if "user" in session:
        ing = Ingredient.get(id)
        ing.delete()
        return redirect(url_for('ingredient.ingredients'))
    return redirect(url_for('user.login'))

@ingredient_views.before_request
def antes_de_iniciar():
    ruta = request.path
    if 'user' not in session and ruta != "/ingredients/" and ruta != "/ingredients/create/" and not ruta.startswith("/static"):
        flash("Es necesario iniciar sesion.")
        return redirect(url_for('user.login'))
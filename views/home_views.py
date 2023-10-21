from flask import Blueprint, render_template, session, redirect, url_for

from models.products import Product
from models.categories import Category

from forms.home_forms import CategoryForm

home_views = Blueprint('home',__name__)


@home_views.route('/')
def index():
    return redirect(url_for('home.home'))

@home_views.route("/home/", methods=["POST", "GET"])
def home():
    categories = Category.get_all()
    cats = [('-1', 'Todos')]
    for category in categories:
        cats.append((category.id, category.category))
    form = CategoryForm()
    form.categories.choices = cats
    if form.validate_on_submit():
        cat_id = form.categories.data
        if cat_id == -1:
            products = Product.get_all(limit=6)
        else:
            products = Product.get_by_category(cat_id)
        form.categories.data = cat_id
        return render_template('home/home.html', products=products, cats=cats, form=form)
    products = Product.get_all(limit=6)
    return render_template('home/home.html', products=products, cats=cats, form=form)

@home_views.route("/contact/")
def contact():
    return render_template('home/contact.html')

@home_views.route('/about/')
def about():
    return render_template('home/about.html')


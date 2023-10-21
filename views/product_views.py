from flask import Blueprint, render_template, redirect, url_for, abort, session, request, flash

from models.products import Product 

from forms.product_forms import UpdateProductForm, CreateProductForm

from models.categories import Category

from utils.file_handler import save_image

product_views = Blueprint('product', __name__)

@product_views.route('/products/')
@product_views.route('/products/<int:page>/')
def home(page=1):
    if "user" in session:
        limit = 10
        products = Product.get_all(limit=limit, page=page)
        total_products = Product.count()
        pages = total_products // limit
        user = session.get("user")
        return render_template('products/product.html', products=products, pages=pages, user=user)
    return redirect(url_for('user.login'))

@product_views.route('/products/<int:page>/')
def next(page=2):
    if "user" in session:
        limit = 10
        products = Product.get_all(limit=limit, page=page)
        total_products = Product.count()
        pages = total_products // limit
        user = session.get("user")
        return render_template('products/product.html', products=products, pages=pages, user=user)
    return redirect(url_for('user.login'))

@product_views.route('/products/create/', methods=('GET', 'POST'))
def create():
    if "user" in session:#Linea de sesion
        form = CreateProductForm()
        if form.validate_on_submit():
            name = form.name.data
            price = form.price.data
            stock = form.stock.data
            size = form.size.data
            category_id = form.category_id.data
            f = form.image.data
            image=""
            if f:
                image = save_image(f, 'images/products')
            product = Product(name=name,
                            price=price,
                            stock=stock,
                            size=size,
                            category_id=category_id,
                            image=image)
            print(product)
            product.save()
            return redirect(url_for('product.home'))
        return render_template('products/create_prod.html', form=form)
    return redirect(url_for('user.login'))#LINEA DE SESION 

@product_views.route('/products/<int:id>/update/', methods=('GET', 'POST'))
def update_prod(id):
    if "user" in session:
        form = UpdateProductForm()
        categories = Category.get_all()
        cats = [(-1, '')]
        for cat in categories:
            cats.append((cat.id, cat.category))
        form.category_id.choices = cats
        product = Product.get(id)
        if product is None:
            abort(404)
        if form.validate_on_submit():
            product.name = form.name.data
            product.size = form.size.data
            product.price = form.price.data
            product.stock = form.stock.data
            product.category_id = form.category_id.data
            f = form.image.data
            if f:
                image = save_image(f, 'images/products')
                product.image = image
            product.save()
            return redirect(url_for('product.home'))
        form.name.data = product.name
        form.size.data = product.size
        form.price.data = product.price
        form.stock.data = product.stock
        form.category_id.data = product.category_id
        image = product.image
        return render_template('products/create_prod.html', form=form, image=image)
    return redirect(url_for('user.login'))


@product_views.route('/products/<int:id>/detail/')
def detail(id):
    if "user" in session:
        product = Product.get(id)
        if product is None: abort(404)
        cat = Category.get(product.category_id)
        return render_template('products/details.html', product=product, cat=cat)
    return redirect(url_for('user.login'))

@product_views.route('/product/<int:id>/delete/', methods=['POST'])
def delete(id):
    if "user" in session:
        product = Product.get(id)
        if product is None:
            abort(404)
        product.delete()
        return redirect(url_for('product.home'))
    return redirect(url_for('user.login'))


@product_views.route('/products/buscar/', methods=['GET','POST'])
def search():
    result = None
    if request.method == "POST":
        result = Product.search(result)
        search  = request.form['buscar']
        return render_template('products/busqueda.html', miData = result, busqueda = search)
    return redirect(url_for('product.home')) 

@product_views.before_request
def antes_de_iniciar():
    ruta = request.path
    if 'user' not in session and ruta != "/products/" and ruta != "/products/create/" and not ruta.startswith("/static"):
        flash("Es necesario iniciar sesion.")
        return redirect(url_for('user.login'))
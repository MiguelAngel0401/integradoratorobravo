from flask import Blueprint, render_template, redirect, url_for, abort, session, request, flash

from models.sells import Sell 

from forms.sell_form import CreateSellForm


sell_views = Blueprint('sell', __name__)

@sell_views.route('/sells/')
@sell_views.route('/sells/<int:page>/', methods=('GET','POST'))
def sells(page=1):
    if "user" in session:
        limit = 10
        sells = Sell.get_all(limit=limit, page=page)
        total_sells = Sell.count()
        pages = total_sells // limit
        user = session.get("user")
        return render_template('sells/sell.html', sells=sells, pages=pages, user=user)
    return redirect(url_for('user.login'))

@sell_views.route('/sells/create/', methods=['GET', 'POST'])
def create_sell():
    if "user" in session:
        form = CreateSellForm()
        if form.validate_on_submit():
            prod_name = form.prod_name.data['user']
            tProduct = form.tProduct.data
            new_sell = Sell(prod_name=prod_name, tProduct=tProduct)
            new_sell.save()
            flash("Venta creada exitosamente", "success")
            return redirect(url_for('sell.sells'))
        
        return render_template('sells/order.html', form=form)
    
    return redirect(url_for('user.login'))

@sell_views.before_request
def antes_de_iniciar():
    ruta = request.path
    if 'user' not in session and ruta != "/sells/" and not ruta.startswith("/static"):
        flash("Es necesario iniciar sesion.")
        return redirect(url_for('user.login'))
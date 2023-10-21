from flask import Blueprint, render_template, redirect, url_for, flash, request, session

from models.promotions import Promotion 

from forms.promotion_forms import UpdatePromotionForm, CreatePromotionForm

promotion_views = Blueprint('promotion', __name__)

@promotion_views.route('/promotions/')
def promotions():
    if "user" in session:
        promotions = Promotion.get_all()
        user = session.get("user")
        return render_template('promotions/promotion.html',
                            promotions=promotions, user=user)
    return redirect(url_for('user.login'))

@promotion_views.route('/promotions/create/', methods=('GET', 'POST'))
def create_prom():
    if "user" in session:
        form = CreatePromotionForm()
        if form.validate_on_submit():
            name = form.name.data
            description = form.description.data
            prom = Promotion(name, description)
            prom.save()
            return redirect(url_for('promotion.promotions'))
        return render_template('promotions/create_prom.html', form=form)
    return redirect(url_for('user.login'))

@promotion_views.route('/promotions/<int:id>/update/', methods=('GET', 'POST'))
def update_prom(id):
    if "user" in session:
        form = UpdatePromotionForm()
        prom = Promotion.get(id)
        if form.validate_on_submit():
            prom.name = form.name.data
            prom.description = form.description.data
            prom.save()
            return redirect(url_for('promotion.promotions'))
        form.name.data = prom.name
        form.description.data = prom.description
        return render_template('promotions/create_prom.html', form=form )
    return redirect(url_for('user.login'))

@promotion_views.route('/promotions/<int:id>/delete/', methods=('GET','POST'))
def delete_prom(id):
    if "user" in session:
        prom = Promotion.get(id)
        prom.delete()
        return redirect(url_for('promotion.promotions'))
    return redirect(url_for('user.login'))

@promotion_views.before_request
def antes_de_iniciar():
    ruta = request.path
    if 'user' not in session and ruta != "/promotions/" and ruta != "/promotions/create/" and not ruta.startswith("/static"):
        flash("Es necesario iniciar sesion.")
        return redirect(url_for('user.login'))
from flask import Blueprint, render_template, redirect, url_for

error_views = Blueprint('error', __name__)

@error_views.app_errorhandler(404)
def not_found_error(error):
    return redirect(url_for('home.home'))

@error_views.app_errorhandler(401)
def not_found_error(error):
    return render_template('error/401.html')

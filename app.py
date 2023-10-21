from flask import Flask

from views.home_views import home_views
from views.category_views import category_views
from views.user_views import user_views
from views.error_views import error_views
from views.ingredient_views import ingredient_views
from views.product_views import product_views
from views.sell_views import sell_views
from views.promotion_views import promotion_views

app = Flask(__name__)

app.config['SECRET_KEY'] = 'My Secret Key'

app.register_blueprint(home_views)
app.register_blueprint(category_views)
app.register_blueprint(user_views)
app.register_blueprint(error_views)
app.register_blueprint(ingredient_views)
app.register_blueprint(product_views)
app.register_blueprint(sell_views)
app.register_blueprint(promotion_views)


if __name__ == '__main__':
    app.run(debug=True)
    
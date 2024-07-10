from flask import Blueprint
from flask_restful import Api
from .user_routes import UserResource
from .order_routes import OrderResource
from .item_routes import ItemResource
from .feedback_routes import FeedbackResource

# Create a blueprint for routes
bp = Blueprint('api', __name__)

# Create an Api instance
api = Api(bp)

# Add resources to the API
api.add_resource(UserResource, '/users', '/users/<int:id>')
api.add_resource(OrderResource, '/orders', '/orders/<int:id>')
api.add_resource(ItemResource, '/items', '/items/<int:id>')
api.add_resource(FeedbackResource, '/feedback', '/feedback/<int:id>')

# You can add more routes here as needed


def init_app(app):
    app.register_blueprint(bp)

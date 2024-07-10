from config import app, api
from routes import user_routes, order_routes, item_routes, feedback_routes

api.add_resource(user_routes.UserResource, '/users', '/users/<int:id>')
api.add_resource(order_routes.OrderResource, '/orders', '/orders/<int:id>')
api.add_resource(item_routes.ItemResource, '/items', '/items/<int:id>')
api.add_resource(feedback_routes.FeedbackResource, '/feedback', '/feedback/<int:id>')

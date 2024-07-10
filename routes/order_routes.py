from flask import request
from flask_restful import Resource
from models import Order
from database import db

class OrderResource(Resource):
    def get(self, id=None):
        if id:
            order = Order.query.get_or_404(id)
            return order.serialize(), 200
        else:
            orders = Order.query.all()
            return [order.serialize() for order in orders], 200

    def post(self):
        data = request.get_json()
        new_order = Order(
            pickup_address=data['pickup_address'],
            delivery_address=data['delivery_address'],
            user_id=data['user_id']  # Assuming user_id is provided in the request
        )
        db.session.add(new_order)
        db.session.commit()
        return new_order.serialize(), 201

    def put(self, id):
        order = Order.query.get_or_404(id)
        data = request.get_json()
        order.pickup_address = data.get('pickup_address', order.pickup_address)
        order.delivery_address = data.get('delivery_address', order.delivery_address)
        order.status = data.get('status', order.status)
        db.session.commit()
        return order.serialize(), 200

    def delete(self, id):
        order = Order.query.get_or_404(id)
        db.session.delete(order)
        db.session.commit()
        return {'message': 'Order deleted successfully'}, 200

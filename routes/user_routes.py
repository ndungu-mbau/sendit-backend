from flask import request
from flask_restful import Resource
from models import db, Item

class ItemResource(Resource):
    def get(self, id=None):
        if id:
            item = Item.query.get_or_404(id)
            return item.serialize(), 200
        else:
            items = Item.query.all()
            return [item.serialize() for item in items], 200

    def post(self):
        data = request.get_json()
        new_item = Item(
            item_name=data['item_name'],
            description=data['description'],
            price=data['price'],
            order_id=data['order_id']
        )
        db.session.add(new_item)
        db.session.commit()
        return new_item.serialize(), 201

    def put(self, id):
        item = Item.query.get_or_404(id)
        data = request.get_json()
        item.item_name = data.get('item_name', item.item_name)
        item.description = data.get('description', item.description)
        item.price = data.get('price', item.price)
        db.session.commit()
        return item.serialize(), 200

    def delete(self, id):
        item = Item.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deleted successfully'}, 200
# from database import db
# from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
# from sqlalchemy.orm import relationship,validates


# class User(db.Model, SerializerMixin):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(60), nullable=False)
#     email = db.Column(db.String(110), unique=True, nullable=False)
#     password = db.Column(db.String(40), nullable=False)
#     role = db.Column(db.String(50), nullable=False)
#     orders = db.relationship('Order', backref='user', lazy=True)

#     serialize_rules = ('-orders.user',)

#     # @validates('email')
#     # def validate_email(self, key, email):
#     #        # Simple regex for validating an Email
#     #     regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#     #     if not re.match(regex, email):
#     #         raise ValueError("Invalid email address")
#     #     return email


# class Order(db.Model, SerializerMixin):
#     __tablename__ = 'orders'
#     order_id = db.Column(db.Integer, primary_key=True)
#     pickup_address = db.Column(db.Text, nullable=False)
#     delivery_address = db.Column(db.Text, nullable=False)
#     status = db.Column(db.String(50), default='pending')
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

#     items = relationship('Item', secondary=order_item_association, backref='orders', lazy='subquery')
#     feedback = relationship('Feedback', backref='order', lazy=True)

#     serialize_rules = ('-items.orders', '-feedback.order',)
#     # items = db.relationship('Item', backref='order', lazy=True)
#     # feedback = db.relationship('Feedback', backref='order', lazy=True)

#     # # serialize_rules = ('-items.order','-feedback.orders')

# class Item(db.Model, SerializerMixin):
#     __tablename__ = 'items'
#     id = db.Column(db.Integer, primary_key=True)
#     item_name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     price = db.Column(db.Integer, nullable=False)

#     serialize_rules = ('-orders.items',)

#     # order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)

# class Feedback(db.Model, SerializerMixin):
#     __tablename__ = 'feedback'
#     id = db.Column(db.Integer, primary_key=True)
#     rating = db.Column(db.Integer, nullable=False)
#     comment = db.Column(db.Text, nullable=False)
#     order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
#     # order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)

#     serialize_rules = ('-order.feedback',)

#     class OrderItem(db.Model):
#         __tablename__ = 'order_item'
#     order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
#     item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)

# # class OrderItem(db.Model):
# #     __tablename__ = 'order_item'
# #     order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True)
# #     item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)




from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from database import db

# Association table
order_item_association = db.Table(
    'order_item_association',
    db.Model.metadata,
    Column('order_id', Integer, ForeignKey('orders.order_id')),
    Column('item_id', Integer, ForeignKey('items.id'))
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(110), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    serialize_rules = ('-orders.user',)
    @db.validates('email')
    def validate_email(self, key, email):
        # Simple regex for validating an Email
        import re
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email

class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    pickup_address = db.Column(db.Text, nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    items = relationship('Item', secondary=order_item_association, backref='orders', lazy='subquery')
    feedback = relationship('Feedback', backref='order', lazy=True)

    serialize_rules = ('-items.orders', '-feedback.order',)

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    serialize_rules = ('-orders.items',)

class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)

    serialize_rules = ('-order.feedback',)


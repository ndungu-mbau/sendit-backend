from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from database import db




# Association table 
order_parcel_association = Table(

    'order_parcel_association',
    db.Model.metadata,
    Column('order_id', Integer, ForeignKey('orders.order_id')),
    Column('parcel_id', Integer, ForeignKey('parcel.id'))
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

    parcels = db.relationship('Parcel', secondary=order_parcel_association, backref='orders', lazy='subquery')
    feedback = db.relationship('Feedback', backref='order', lazy=True)

    serialize_rules = ('-parcel.orders', '-feedback.order',)

    class Profile(db.Model):
        __tablename__ = 'profiles'

        id = db.Column(db.Integer, primary_key=True)
        profile_picture = db.Column(db.String(255))
        location = db.Column(db.String)
        created_at = db.Column(db.DateTime, default=db.func.now())
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        users = db.relationship('User', backref='profiles')
        serialize_rules = ('-users.profiles',)

class Parcel(db.Model):
  _tablename_ = 'parcels'

  id = db.Column(db.Integer, primary_key=True)
  pickup_location = db.Column(db.String)
  destination = db.Column(db.String)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  weight = db.Column(db.Float, nullable=False)
  price = db.Column(db.Float, nullable=True)
  description = db.Column(db.String)

  users = db.relationship('User', backref='parcels')
  serialize_rules = ('-users.parcels',)

# class Item(db.Model, SerializerMixin):
#     __tablename__ = 'items'
#     id = db.Column(db.Integer, primary_key=True)
#     item_name = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     price = db.Column(db.Integer, nullable=False)

#     serialize_rules = ('-orders.items',)

class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    order_id = db.Column(Integer, ForeignKey('orders.order_id'), nullable=False)

    serialize_rules = ('-order.feedback',)


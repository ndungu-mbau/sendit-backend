from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from database import db


# order_parcel_association = db.Table(
#     'order_parcel_association',
#     db.Model.metadata,
#     Column('order_id', Integer, ForeignKey('orders.order_id')),
#     Column('parcel_id', Integer, ForeignKey('parcels.id'))
# )

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-orders.user', '-parcels.user', '-password',)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(110), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)
    parcels = db.relationship('Parcel', backref='user', lazy=True)


    @db.validates('email')
    def validate_email(self, key, email):
        import re
        regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, email):
            raise ValueError("Invalid email address")
        return email

class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'
    serialize_rules = ('-user.orders', '-parcels.orders', '-feedback.order',)
    order_id = db.Column(db.Integer, primary_key=True)
    pickup_address = db.Column(db.Text, nullable=False)
    delivery_address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='pending')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # parcels = relationship('Parcel', secondary=order_parcel_association, backref='orders', lazy='subquery')
    feedback = relationship('Feedback', backref='order', lazy=True)


class Parcel(db.Model, SerializerMixin):
    __tablename__ = 'parcels'

    serialize_rules = ('-user.parcels', '-orders.parcels',)
    id = db.Column(db.Integer, primary_key=True)
    pickup_location = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    weight = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=True)
    description = db.Column(db.String)


class Profile(db.Model,SerializerMixin):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(db.String(255))
    location = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='profiles')

    serialize_rules = ('-user.profiles',)



class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedback'

    serialize_rules = ('-order.feedback',)
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)


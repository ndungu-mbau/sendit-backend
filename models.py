from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy_serializer import SerializerMixin


Base = declarative_base()


order_parcel_association = Table(
    'order_parcel_association',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.order_id')),
    Column('parcel_id', Integer, ForeignKey('parcels.id'))
)

class User(Base, SerializerMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(60), nullable=False)
    email = Column(String(110), unique=True, nullable=False)
    password = Column(String(40), nullable=False)
    role = Column(String(50), nullable=False)

    orders = relationship('Order', backref='user', lazy=True)
    parcels_list = relationship('Parcel', backref='owner', lazy=True)
    profiles = relationship('Profile', back_populates='user', lazy=True)

    serialize_rules = ('-orders.user', '-parcels_list.owner', '-profiles.user',)

class Order(Base, SerializerMixin):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    pickup_address = Column(Text, nullable=False)
    delivery_address = Column(Text, nullable=False)
    status = Column(String(50), default='pending')
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    parcels = relationship('Parcel', secondary=order_parcel_association, backref='orders', lazy='subquery')
    feedback = relationship('Feedback', backref='order', lazy=True)

    serialize_rules = ('-parcels.orders', '-feedback.order',)

class Parcel(Base, SerializerMixin):
    __tablename__ = 'parcels'
    id = Column(Integer, primary_key=True)
    pickup_location = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    weight = Column(Float, nullable=False)
    price = Column(Float, nullable=True)
    description = Column(String)

    user = relationship('User', back_populates='parcels_list')  # Update this line

    serialize_rules = ('-user.parcels_list',)

class Profile(Base, SerializerMixin):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    full_name = Column(String(100), nullable=False)
    bio = Column(String(255))
    profile_picture = Column(String(255))
    location = Column(String(100))

    user = relationship('User', back_populates='profiles')

    serialize_rules = ('-user.profiles',)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'bio': self.bio,
            'profile_picture': self.profile_picture,
            'location': self.location,
            'user_id': self.user_id
        }

class Feedback(Base, SerializerMixin):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)

    serialize_rules = ('-order.feedback',)

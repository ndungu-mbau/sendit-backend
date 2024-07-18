from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from database import db
from models import User, Order, Feedback, Parcel, Profile

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return "<h1>Welcome to the Parcel Pro App</h1>"

# Routes for Users
class Users(Resource):
    def get(self):
        users = User.query.all()
        users_list = [user.to_dict() for user in users]
        return make_response(jsonify({"count": len(users_list), "users": users_list}), 200)

    def post(self):
        new_user = User(
            username=request.json.get("username"),
            email=request.json.get("email"),
            password=request.json.get("password"),
            role=request.json.get("role")
        )
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify(new_user.to_dict()), 201)

api.add_resource(Users, '/users')

class UserByID(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)
        return make_response(jsonify(user.to_dict()), 200)

    def patch(self, id):
        user = User.query.get(id)
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)
        for attr in request.json:
            setattr(user, attr, request.json.get(attr))
        db.session.commit()
        return make_response(jsonify(user.to_dict()), 200)

    def delete(self, id):
        user = User.query.get(id)
        if user is None:
            return make_response(jsonify({"message": "User not found"}), 404)
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message": "User deleted"}), 200)

api.add_resource(UserByID, '/users/<int:id>')

# Routes for Orders
class Orders(Resource):
    def get(self):
        orders = Order.query.all()
        orders_list = [order.to_dict() for order in orders]
        return make_response(jsonify({"count": len(orders_list), "orders": orders_list}), 200)

    def post(self):
        new_order = Order(
            pickup_address=request.json.get("pickup_address"),
            delivery_address=request.json.get("delivery_address"),
            status=request.json.get("status"),
            user_id=request.json.get("user_id")
        )
        db.session.add(new_order)
        db.session.commit()
        return make_response(jsonify(new_order.to_dict()), 201)

api.add_resource(Orders, '/orders')

class OrderByID(Resource):
    def get(self, id):
        order = Order.query.get(id)
        if order is None:
            return make_response(jsonify({"message": "Order not found"}), 404)
        return make_response(jsonify(order.to_dict()), 200)

    def patch(self, id):
        order = Order.query.get(id)
        if order is None:
            return make_response(jsonify({"message": "Order not found"}), 404)
        for attr in request.json:
            setattr(order, attr, request.json.get(attr))
        db.session.commit()
        return make_response(jsonify(order.to_dict()), 200)

    def delete(self, id):
        order = Order.query.get(id)
        if order is None:
            return make_response(jsonify({"message": "Order not found"}), 404)
        db.session.delete(order)
        db.session.commit()
        return make_response(jsonify({"message": "Order deleted"}), 200)

api.add_resource(OrderByID, '/orders/<int:id>')

# Routes for Parcels
class Parcels(Resource):
    def get(self):
        parcels = Parcel.query.all()
        parcels_list = [parcel.to_dict() for parcel in parcels]
        return make_response(jsonify({"count": len(parcels_list), "parcels": parcels_list}), 200)

    def post(self):
        new_parcel = Parcel(
            pickup_location=request.json.get("pickup_location"),
            destination=request.json.get("destination"),
            user_id=request.json.get("user_id"),
            weight=request.json.get("weight"),
            price=request.json.get("price"),
            description=request.json.get("description")
        )
        db.session.add(new_parcel)
        db.session.commit()
        return make_response(jsonify(new_parcel.to_dict()), 201)

api.add_resource(Parcels, '/parcels')

class ParcelByID(Resource):
    def get(self, id):
        parcel = Parcel.query.get(id)
        if parcel is None:
            return make_response(jsonify({"message": "Parcel not found"}), 404)
        return make_response(jsonify(parcel.to_dict()), 200)

    def patch(self, id):
        parcel = Parcel.query.get(id)
        if parcel is None:
            return make_response(jsonify({"message": "Parcel not found"}), 404)
        for attr in request.json:
            setattr(parcel, attr, request.json.get(attr))
        db.session.commit()
        return make_response(jsonify(parcel.to_dict()), 200)

    def delete(self, id):
        parcel = Parcel.query.get(id)
        if parcel is None:
            return make_response(jsonify({"message": "Parcel not found"}), 404)
        db.session.delete(parcel)
        db.session.commit()
        return make_response(jsonify({"message": "Parcel deleted"}), 200)


api.add_resource(ParcelByID, '/parcels/<int:id>')

# Routes for Feedback
class Feedbacks(Resource):
    def get(self):
        feedbacks = Feedback.query.all()
        feedbacks_list = [feedback.to_dict() for feedback in feedbacks]
        return make_response(jsonify({"count": len(feedbacks_list), "feedbacks": feedbacks_list}), 200)

    def post(self):
        new_feedback = Feedback(
            rating=request.json.get("rating"),
            comment=request.json.get("comment"),
            order_id=request.json.get("order_id")
        )
        db.session.add(new_feedback)
        db.session.commit()
        return make_response(jsonify(new_feedback.to_dict()), 201)

api.add_resource(Feedbacks, '/feedbacks')

class FeedbackByID(Resource):
    def get(self, id):
        feedback = Feedback.query.get(id)
        if feedback is None:
            return make_response(jsonify({"message": "Feedback not found"}), 404)
        return make_response(jsonify(feedback.to_dict()), 200)

    def patch(self, id):
        feedback = Feedback.query.get(id)
        if feedback is None:
            return make_response(jsonify({"message": "Feedback not found"}), 404)
        for attr in request.json:
            setattr(feedback, attr, request.json.get(attr))
        db.session.commit()
        return make_response(jsonify(feedback.to_dict()), 200)

    def delete(self, id):
        feedback = Feedback.query.get(id)
        if feedback is None:
            return make_response(jsonify({"message": "Feedback not found"}), 404)
        db.session.delete(feedback)
        db.session.commit()
        return make_response(jsonify({"message": "Feedback deleted"}), 200)

api.add_resource(FeedbackByID, '/feedbacks/<int:id>')

# Routes for Profiles
class Profiles(Resource):
    def get(self):
        profiles = Profile.query.all()
        profiles_list = [profile.to_dict() for profile in profiles]
        return make_response(jsonify({"count": len(profiles_list), "profiles": profiles_list}), 200)

    def post(self):
        new_profile = Profile(
            profile_picture=request.json.get("profile_picture"),
            location=request.json.get("location"),
            user_id=request.json.get("user_id")
        )
        db.session.add(new_profile)
        db.session.commit()
        return make_response(jsonify(new_profile.to_dict()), 201)

api.add_resource(Profiles, '/profiles')

class ProfileByID(Resource):
    def get(self, id):
        profile = Profile.query.get(id)
        if profile is None:
            return make_response(jsonify({"message": "Profile not found"}), 404)
        return make_response(jsonify(profile.to_dict()), 200)

    def patch(self, id):
        profile = Profile.query.get(id)
        if profile is None:
            return make_response(jsonify({"message": "Profile not found"}), 404)
        for attr in request.json:
            setattr(profile, attr, request.json.get(attr))
        db.session.commit()
        return make_response(jsonify(profile.to_dict()), 200)

    def delete(self, id):
        profile = Profile.query.get(id)
        if profile is None:
            return make_response(jsonify({"message": "Profile not found"}), 404)
        db.session.delete(profile)
        db.session.commit()
        return make_response(jsonify({"message": "Profile deleted"}), 200)

api.add_resource(ProfileByID, '/profiles/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
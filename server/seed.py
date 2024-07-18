from faker import Faker
from app import app
from database import db
from models import User, Order, Parcel, Profile, Feedback

fake = Faker()

def seed_data():
    with app.app_context():
        
        db.drop_all()
        db.create_all()


        users = []
        for _ in range(5):
            user = User(
                username=fake.user_name(),
                email=fake.unique.email(),
                password=fake.password(length=12),
                role=fake.random_element(elements=('admin', 'customer'))
            )
            users.append(user)
        db.session.add_all(users)
        db.session.commit()


        orders = []
        for _ in range(5):
            order = Order(
                pickup_address=fake.address(),
                delivery_address=fake.address(),
                status=fake.random_element(elements=('pending', 'shipped', 'delivered', 'canceled')),
                user_id=fake.random_element(elements=[user.id for user in users])
            )
            orders.append(order)
        db.session.add_all(orders)
        db.session.commit()


        parcels = []
        for _ in range(10):
            parcel = Parcel(
                pickup_location=fake.address(),
                destination=fake.address(),
                user_id=fake.random_element(elements=[user.id for user in users]),
                weight=fake.random_number(digits=2),
                price=fake.random_number(digits=3),
                description=fake.text(max_nb_chars=200)
            )
            parcels.append(parcel)
        db.session.add_all(parcels)
        db.session.commit()


        # for order in orders:
        #     associated_parcels = fake.random_elements(elements=[parcel.id for parcel in parcels], unique=True, length=fake.random_int(min=1, max=3))
        #     for parcel_id in associated_parcels:
        #         db.session.execute(order_parcel_association.insert().values(order_id=order.order_id, parcel_id=parcel_id))
        # db.session.commit()


        profiles = []
        for user in users:
            profile = Profile(
                profile_picture=fake.image_url(),
                location=fake.city(),
                user_id=user.id
            )
            profiles.append(profile)
        db.session.add_all(profiles)
        db.session.commit()


        feedbacks = []
        for _ in range(5):
            feedback = Feedback(
                rating=fake.random_int(min=1, max=5),
                comment=fake.text(max_nb_chars=200),
                order_id=fake.random_element(elements=[order.order_id for order in orders])
            )
            feedbacks.append(feedback)
        db.session.add_all(feedbacks)
        db.session.commit()

if __name__ == "__main__":
    seed_data()
    print("Seeding complete!")

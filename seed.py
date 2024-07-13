
from faker import Faker

from app import app, db
from models import User, Order, Item, Feedback, order_item_association
from sqlalchemy.exc import IntegrityError


fake = Faker()

def seed_data():
    with app.app_context():
        try:


# Function to seed data
def seed_data():
    with app.app_context():
        try:
            # Reset the database
            reset_database()

            # Create sample users
            user1 = User(username='john_doe', email='john@example.com', password='password123', role='admin')
            user2 = User(username='jane_doe', email='jane@example.com', password='password123', role='user')
            user3 = User(username='mercy_grace', email='mercy@example.com', password='password123', role='admin')

            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            db.session.commit()


            User.query.delete()
            Order.query.delete()
            Item.query.delete()
            Feedback.query.delete()


            users = []
            for _ in range(10):
                username = fake.user_name()
                domain = fake.free_email_domain()
                email = f"{username}@{domain}"
                password = fake.password(length=12)
                role = fake.random_element(elements=['admin', 'user'])
                users.append(User(username=username, email=email, password=password, role=role))

            db.session.add_all(users)
            db.session.commit()


            items = []
            for _ in range(10):
                items.append(Item(
                    item_name=fake.word(),
                    description=fake.text(),
                    price=fake.random_number(digits=3, fix_len=False)
                ))

            db.session.add_all(items)
            db.session.commit()



            orders = []
            for user in users:
                for _ in range(2):
                    order = Order(
                        pickup_address=fake.address(),
                        delivery_address=fake.address(),
                        user_id=user.id
                    )
                    orders.append(order)
                    db.session.add(order)

                    # Adding items
                    order_items = fake.random_elements(elements=[item.id for item in items], length=2, unique=True)
                    for item_id in order_items:
                        db.session.execute(order_item_association.insert().values(order_id=order.order_id, item_id=item_id))

            db.session.commit()

            # Create Feedback
            feedbacks = []
            for order in orders:
                feedbacks.append(Feedback(
                    rating=fake.random_int(min=1, max=5),
                    comment=fake.sentence(),
                    order_id=order.order_id
                ))

            db.session.add_all(feedbacks)

            # Associate items with orders
            order1.items.append(item1)
            order2.items.append(item2)
            order3.items.append(item3)
            db.session.commit()

            # Create sample feedback
            feedback1 = Feedback(rating=5, comment='Excellent service!', order_id=order1.order_id)
            feedback2 = Feedback(rating=4, comment='Very good, but could be improved.', order_id=order2.order_id)
            feedback3 = Feedback(rating=3, comment='Average experience.', order_id=order3.order_id)

            db.session.add(feedback1)
            db.session.add(feedback2)
            db.session.add(feedback3)

            db.session.commit()

            print("Seed data inserted successfully.")

        except IntegrityError as e:
            db.session.rollback()
            print(f"Error inserting seed data: {e}")

if __name__ == '__main__':
    seed_data()

from app import app, db
from models import User, Order, Item, Feedback
from sqlalchemy.exc import IntegrityError


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

            # Create sample items
            item1 = Item(item_name='Laptop', description='A high-end laptop', price=1500)
            item2 = Item(item_name='Smartphone', description='A latest model smartphone', price=800)
            item3 = Item(item_name='Headphones', description='High-quality headphones', price=200)

            db.session.add(item1)
            db.session.add(item2)
            db.session.add(item3)
            db.session.commit()

            # Create sample orders
            order1 = Order(pickup_address='123 Main St', delivery_address='456 Elm St', user_id=user1.id)
            order2 = Order(pickup_address='789 Oak St', delivery_address='101 Pine St', user_id=user2.id)
            order3 = Order(pickup_address='345 Maple St', delivery_address='678 Cherry St', user_id=user3.id)

            db.session.add(order1)
            db.session.add(order2)
            db.session.add(order3)
            db.session.commit()

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

# Run seed function
if __name__ == '__main__':
    seed_data()

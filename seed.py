from flask import current_app
from models import db, User, Order, Item

def seed_data():
    # Sample data to seed into the database
    users_data = [
        {
            'username': 'user1',
            'email': 'user1@example.com',
            'password': 'password1',
            'role': 'user'
        },
        {
            'username': 'user2',
            'email': 'user2@example.com',
            'password': 'password2',
            'role': 'admin'
        }
    ]

    orders_data = [
        {
            'pickup_address': 'Address 1',
            'delivery_address': 'Address 2',
            'status': 'pending',
            'user_id': 1  # User ID for user1
        },
        {
            'pickup_address': 'Address 3',
            'delivery_address': 'Address 4',
            'status': 'completed',
            'user_id': 2  # User ID for user2
        }
    ]

    # Create instances of User and add them to the session
    for user_info in users_data:
        user = User(
            username=user_info['username'],
            email=user_info['email'],
            password=user_info['password'],
            role=user_info['role']
        )
        db.session.add(user)

    # Create instances of Order and add them to the session
    for order_info in orders_data:
        order = Order(
            pickup_address=order_info['pickup_address'],
            delivery_address=order_info['delivery_address'],
            status=order_info['status'],
            user_id=order_info['user_id']
        )
        db.session.add(order)

    # Commit all changes to the database
    db.session.commit()

if __name__ == '__main__':
    with current_app.app_context():
        # Ensure the database tables are created before seeding
        db.create_all()
        # Seed data into the database
        seed_data()

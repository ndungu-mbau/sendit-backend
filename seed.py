from flask import current_app
from models import db, Item

def seed_items():
    # Sample data to seed into the database
    items_data = [
        {
            'item_name': 'Keyboard',
            'description': 'Mechanical keyboard with RGB lighting.',
            'price': 99.99,
            'order_id': 1
        },
        {
            'item_name': 'Mouse',
            'description': 'Wireless gaming mouse with adjustable DPI.',
            'price': 49.99,
            'order_id': 2
        },
        # Add more items as needed
    ]

    # Create instances of Item and add them to the session
    for item_info in items_data:
        item = Item(
            item_name=item_info['item_name'],
            description=item_info['description'],
            price=item_info['price'],
            order_id=item_info['order_id']
        )
        db.session.add(item)

    # Commit all changes to the database
    db.session.commit()

if __name__ == '__main__':
    with current_app.app_context():
        # Ensure the database tables are created before seeding
        db.create_all()
        # Seed items into the database
        seed_items()

from faker import Faker
from app import app, db
from models import User, Order, Item, Feedback, order_item_association
from sqlalchemy.exc import IntegrityError

fake = Faker()

def seed_data():
    with app.app_context():
        try:
            
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
            db.session.commit()

            print("Seed data inserted successfully.")

        except IntegrityError as e:
            db.session.rollback()
            print(f"Error inserting seed data: {e}")

if __name__ == '__main__':
    seed_data()

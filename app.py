from flask import Flask
from config import db

app = Flask(__name__)
db.init_app(app)

from routes import user_routes, order_routes, item_routes, feedback_routes

if __name__ == '__main__':
    app.run(debug=True)
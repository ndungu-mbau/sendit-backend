## Description
The SEND IT app is a web application built with Flask and SQLAlchemy, designed to manage parcels, orders, users, profiles, and feedback. This app provides a RESTful API for CRUD (Create, Read, Update, Delete) operations on these entities.

## Installation

1. Clone the repository


git clone https://github.com/kimwereafk/SendIT-backend

cd SendIT-backend

## Installing dependancies
pip install -r requirements.txt

## Initialize the database

flask db init
flask db migrate
flask db upgrade

## Seed the Database

python seed.py

## Running the application
python app.py
https://github.com/kimwereafk/Parcel-Pro-backend.git




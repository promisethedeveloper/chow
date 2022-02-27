from models import db, User, Business, favorites
from app import app

# Drop all tables in the database
db.drop_all()
# Create all database tables
db.create_all()

# Delete all data in the User model
User.query.delete()
Business.query.delete()
favorites.delete()


u1 = User.register(first_name="Promise", last_name="Morka", email="onyekamorka06@yahoo.com", password="1234yes")

db.session.add(u1)
db.session.commit()
"""User model tests."""

# run these test like 

# python -m unittest test_user_model.py

from unittest import TestCase

from flask import session

from app import app 

from models import db, User, Business, favorites

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already been
# connected to the database

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///first_capstone_db_test"
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class BusinessModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        Business.query.delete()

        u1 = User.register("test1_firstname", "test1_lastname", "email1@email.com", "password")
        u1d1 = 77777
        u1.id = u1d1
        
        db.session.add(u1)

        db.session.commit()

        u1 = User.query.get(u1d1)

        self.u1 = u1

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_business_model(self):
        """Does business model work?"""

        b = Business(business_yelp_id = "xyz123")
    
        db.session.add(b)
        db.session.commit()

        # Business model correctly saves API id
        self.assertEqual(b.business_yelp_id, "xyz123")
        self.assertEqual(b.id, 1)
        




   






"""User model tests."""

# run these test like 

# python -m unittest test_user_model.py

from unittest import TestCase

from app import app 

from sqlalchemy import exc


from models import db, User, Business, favorites

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already been
# connected to the database

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///first_capstone_db_test"
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        User.query.delete()

        u1 = User.register("test_firstname", "test_lastname", "email1@email.com", "password")
        u1d1 = 1111
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

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            first_name="test_firstname",
            last_name="test_lastname",
            email="email@email.com",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no businesses
        self.assertEqual(len(u.businesses), 0)
        # User should have an id of 1
        self.assertEqual((u.id), 1)

    ####
    #
    # Signup Tests
    #
    ####
    def test_valid_signup(self):
        u_test = User.register("testtestfirstname", "testtestlastname", "testemail@email.com", "password")
        uid = 99999
        u_test.id = uid
        db.session.add(u_test)
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.first_name, "testtestfirstname")
        self.assertEqual(u_test.last_name, "testtestlastname")
        self.assertEqual(u_test.email, "testemail@email.com")
        # Bycrpt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))


    def test_invalid_firstname_register(self):
        invalid = User.register(None, "testuserlastname", "test@testing.com", "password")
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_lastname_register(self):
        invalid = User.register("testuserlastname", None, "test@testing.com", "password")
        uid = 1234
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_email_register(self):
        invalid = User.register("testuserlastname", "testuserlastname", None, "password")
        uid = 6789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.add(invalid)
            db.session.commit()

    def test_invalid_password_register(self):
        with self.assertRaises(ValueError) as context:
            User.register("testtestfirstname", "testtestlastname", "email@email.com", "")

        with self.assertRaises(ValueError) as context:
            User.register("testtestfirstname", "testtestlastname", "email@email.com", None)
       

    ####
    #
    # Authentication Tests
    #
    ####
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.email, "password")
        self.assertIsNotNone(u)

    def test_invalid_email(self):
        self.assertFalse(User.authenticate("bademail", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.email, "badpassword"))

    






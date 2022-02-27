import email
from flask import session
from app import app
from unittest import TestCase

class HomePageViewsTestCase(TestCase):

    def test_homepage(self):
        """Testing the home route when User is NOT registered yet."""
        with app.test_client() as client:
            res = client.get("/")

            self.assertEqual(session.get("user_id"), None)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/half-homepage")


        """Testing the home route when User is registered."""
        with app.test_client() as client:
            with client.session_transaction() as set_session:
                set_session["user_id"] = 1
            res = client.get("/")
            html = res.get_data(as_text=True)

            self.assertEqual(session.get("user_id"), 1)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3 class="welcome">African Restaurants and Stores, closest to you</h3>', html)


    """Testing the half home page route."""
    def test_half_home_page(self):
        with app.test_client() as client:
            res = client.get("/half-homepage")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="capstone__heading">CAPSTONE PROJECT</h1>', html)


    """Testing the full home page route."""
    def test_full_home_page(self):
        """Testing when User is NOT logged in"""
        with app.test_client() as client:
            res = client.get("/full-homepage")

            self.assertEqual(session.get("user_id"), None)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/half-homepage")

        """Testing when User is logged in"""
        with app.test_client() as client:
            with client.session_transaction() as set_session:
                set_session["user_id"] = 1

            res = client.get("/full-homepage")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3 class="welcome">African Restaurants and Stores, closest to you</h3>', html)
            self.assertEqual(session["user_id"], 1)


    """Testing the signup route"""
    def test_signup_route(self):
        with app.test_client() as client:
            res = client.get("/signup")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="sign__up">Signup</h1>', html)

    def test_signup_route_post(self):
        with app.test_client() as client:

            res = client.post("/signup", data=dict(
                                        first_name="first_name", 
                                        last_name="last_name",
                                        email="123abc@gmail.com",
                                        password="123abc"))

            self.assertEqual(res.status_code, 200)

    """Testing the login route"""
    def test_login_route(self):
        with app.test_client() as client:
            res = client.get("/login")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h5>New to Chow? <a href="/signup">Signup here</a></h5>', html)


    """Testing the logout route"""
    def test_logout_route(self):
        with app.test_client() as client:
            """Remove the user id from session"""
            with client.session_transaction() as set_session:
                set_session["user_id"] = None

            res = client.get("/logout")

            self.assertEqual(session.get("user_id"), None)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/")



    




    

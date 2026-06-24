import unittest
import os
from app import app, init_db


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.db = "test_users.db"

        if os.path.exists(self.db):
            os.remove(self.db)

        init_db(self.db)

        app.config["TESTING"] = True
        app.config["DATABASE"] = self.db

        self.client = app.test_client()

    def tearDown(self):
        if os.path.exists(self.db):
            os.remove(self.db)

    def test_register_verify_login_logout(self):

        # Register
        res = self.client.post(
            "/register",
            data={
                "username": "T",
                "email": "t@example.com",
                "mobile": "9876543210",
                "password": "pass"
            },
            follow_redirects=True
        )

        self.assertEqual(res.status_code, 200)

        # Login
        res2 = self.client.post(
            "/login",
            data={
                "identifier": "t@example.com",
                "password": "pass"
            },
            follow_redirects=True
        )

        self.assertEqual(res2.status_code, 200)

        # Logout
        res3 = self.client.get(
            "/logout",
            follow_redirects=False
        )

        self.assertEqual(res3.status_code, 302)


if __name__ == "__main__":
    unittest.main()
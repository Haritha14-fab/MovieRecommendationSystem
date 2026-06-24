import unittest
from app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home(self):

        with self.client.session_transaction() as sess:

            sess["user"] = {
                "id": 1,
                "name": "Test User",
                "email": "test@example.com",
                "role": "user"
            }

        r = self.client.get("/")

        self.assertEqual(r.status_code, 200)

    def test_recommend_user(self):

        r = self.client.get(
            "/api/recommend_user?topn=3"
        )

        self.assertEqual(
            r.status_code,
            200
        )

        data = r.get_json()

        self.assertIsNotNone(data)

        self.assertIn(
            "recommendations",
            data
        )

    def test_recommend_ai(self):

        r = self.client.get(
            "/api/recommend_ai?title=Toy%20Story%20(1995)&topn=3"
        )

        self.assertEqual(
            r.status_code,
            200
        )

        data = r.get_json()

        self.assertIsNotNone(data)

        self.assertIn(
            "results",
            data
        )

    def test_poster(self):

        r = self.client.get(
            "/api/poster?title=Toy%20Story%20(1995)"
        )

        self.assertEqual(
            r.status_code,
            200
        )

        data = r.get_json()

        self.assertIsNotNone(data)

        self.assertIn(
            "url",
            data
        )


if __name__ == "__main__":
    unittest.main()
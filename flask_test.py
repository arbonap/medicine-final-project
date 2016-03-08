import os
from server import app
import unittest
import tempfile
from model import connect_to_db, db, example_data


class FlaskNoDatabaseTestCase(unittest.TestCase):

    def setUp(self):
      """Stuff to do before every test."""

      self.client = app.test_client()
      app.config['TESTING'] = True

    def test_route(self):
        rv = self.client.get('/sign-up')
        assert "Password" in rv.data
        assert rv.status_code == 200


class FlaskDatabaseTestCase(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):

        result = self.client.post("/loggedin", {'email': '123', 'password': '123'})
        assert result.status_code == 302
        assert "/login" in result.data


if __name__ == '__main__':
    unittest.main()

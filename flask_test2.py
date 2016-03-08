import os
from server import app
import unittest
import tempfile
from model import connect_to_db, db


class FlaskrTestCase1(unittest.TestCase):

    def setUp(self):
      """Stuff to do before every test."""

      self.client = app.test_client()
      app.config['TESTING'] = True

    def test_route(self):
        rv = self.client.get('/sign-up')
        assert "Password" in rv.data
        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()

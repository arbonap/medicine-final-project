import os
from server import app
import unittest
import tempfile
from model import connect_to_db, db


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['medicines'] = tempfile.mkstemp()
        self.app = app.test_client()
        connect_to_db(app, "sqlite:///")
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['medicines'])

    def test_empty_db(self):
        rv = self.app.get('/')
        print rv.status_code
        assert rv.status_code == 200


if __name__ == '__main__':
    unittest.main()

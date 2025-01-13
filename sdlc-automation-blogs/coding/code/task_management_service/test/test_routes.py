import unittest
import json
from app import app, db

class TaskManagementTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/test_db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_task(self):
        response = self.app.post('/tasks', json={
            'title': 'Test Task',
            'description': 'This is a test task',
            'status': 'Open',
            'priority': 'High'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_task(self):
        self.app.post('/tasks', json={'title': 'Test Task', 'status': 'Open'})
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
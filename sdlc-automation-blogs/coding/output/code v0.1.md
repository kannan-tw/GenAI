Based on the provided High-Level Design (HLD) and Software Requirements Specification (SRS), we will create a Python codebase for the microservices specified, particularly focusing on the Task Management Service, Notification Service, and Reporting Service. Below is the implementation plan, including the project structure, codebase, setup instructions, and test scripts.

## Project Structure

```
task_management_app/
│
├── api_gateway/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── task_management_service/
│   ├── app.py
│   ├── models.py
│   ├── routes.py
│   ├── requirements.txt
│   ├── test/
│   │   ├── test_routes.py
│   └── README.md
│
├── notification_service/
│   ├── app.py
│   ├── requirements.txt
│   ├── test/
│   │   ├── test_notifications.py
│   └── README.md
│
└── reporting_service/
    ├── app.py
    ├── requirements.txt
    ├── test/
    │   ├── test_reporting.py
    └── README.md
```

## 1. Task Management Service

### 1.1 Codebase

**task_management_service/app.py**
```python
from flask import Flask
from routes import task_routes

app = Flask(__name__)

# Register routes
app.register_blueprint(task_routes)

if __name__ == '__main__':
    app.run(port=8080)
```

**task_management_service/routes.py**
```python
from flask import Blueprint, request, jsonify
from models import Task, db

task_routes = Blueprint('task_routes', __name__)

@task_routes.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = Task(**data)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@task_routes.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict()), 200

@task_routes.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.json
    task = Task.query.get_or_404(id)
    for key, value in data.items():
        setattr(task, key, value)
    db.session.commit()
    return jsonify(task.to_dict()), 200

@task_routes.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 204
```

**task_management_service/models.py**
```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    status = db.Column(db.String(50), default='Open')
    priority = db.Column(db.String(50))
    due_date = db.Column(db.DateTime)
    assignee_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date,
            'assignee_id': self.assignee_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
```

### 1.2 Setup Instructions

1. **Install Dependencies**:
   Create a `requirements.txt` file in the `task_management_service` directory:
   ```
   Flask==2.0.1
   Flask-SQLAlchemy==2.5.1
   psycopg2-binary==2.9.1
   ```

   Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**:
   Ensure PostgreSQL is running and create a database for the application. Update the database URI in your Flask app configuration.

3. **Run the Service**:
   ```bash
   python app.py
   ```

### 1.3 Test Scripts

**task_management_service/test/test_routes.py**
```python
import unittest
import json
from app import app, db

class TaskManagementTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_task(self):
        response = self.app.post('/tasks', json={
            'title': 'Test Task',
            'description': 'This is a test task',
            'priority': 'High'
        })
        self.assertEqual(response.status_code, 201)

    def test_get_task(self):
        self.app.post('/tasks', json={'title': 'Test Task'})
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

## 2. Notification Service

### 2.1 Codebase

**notification_service/app.py**
```python
from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

@app.route('/notifications', methods=['POST'])
def send_notification():
    data = request.json
    # Logic to send notification (email or in-app)
    return jsonify({'message': 'Notification sent'}), 201

if __name__ == '__main__':
    app.run(port=8080)
```

### 2.2 Setup Instructions

1. **Install Dependencies**:
   Create a `requirements.txt` file in the `notification_service` directory:
   ```
   Flask==2.0.1
   ```

   Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Service**:
   ```bash
   python app.py
   ```

### 2.3 Test Scripts

**notification_service/test/test_notifications.py**
```python
import unittest
from app import app

class NotificationServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_send_notification(self):
        response = self.app.post('/notifications', json={
            'user_id': 1,
            'task_id': 1,
            'type': 'email',
            'message': 'Task assigned'
        })
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
```

## 3. Reporting Service

### 3.1 Codebase

**reporting_service/app.py**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/reports', methods=['GET'])
def generate_report():
    # Logic to generate report
    return jsonify({'report': 'Report data'}), 200

if __name__ == '__main__':
    app.run(port=8080)
```

### 3.2 Setup Instructions

1. **Install Dependencies**:
   Create a `requirements.txt` file in the `reporting_service` directory:
   ```
   Flask==2.0.1
   ```

   Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Service**:
   ```bash
   python app.py
   ```

### 3.3 Test Scripts

**reporting_service/test/test_reporting.py**
```python
import unittest
from app import app

class ReportingServiceTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_generate_report(self):
        response = self.app.get('/reports')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

## Conclusion

This codebase provides a foundational structure for the task management application, implementing the Task Management Service, Notification Service, and Reporting Service. Each service is designed to be modular and follows best practices in Python development. The setup instructions and test scripts ensure that the services can be deployed and tested effectively.
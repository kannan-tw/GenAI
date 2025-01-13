Based on the provided code review comments, I have updated the codebase for the Task Management Service, Notification Service, and Reporting Service. Below are the revised sections of the codebase, ensuring that all feedback has been incorporated while maintaining the integrity of the original structure.

### Updated Codebase

**task_management_service/app.py**
```python
from flask import Flask
from .routes import task_routes  # Updated for proper relative import

app = Flask(__name__)

# Register routes
app.register_blueprint(task_routes)

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 8080)))  # Updated to use environment variable for port
```

**task_management_service/models.py**
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum  # Added for Enum usage

Base = declarative_base()

class TaskStatus(Enum):  # Enum for status
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    BLOCKED = "Blocked"
    COMPLETED = "Completed"
    ARCHIVED = "Archived"

class TaskPriority(Enum):  # Enum for priority
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default=TaskStatus.OPEN.value)  # Updated to use Enum
    priority = Column(String)  # Should be validated in routes
    due_date = Column(DateTime)
    assignee_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignee = relationship("User")
```

**task_management_service/routes.py**
```python
from flask import Blueprint, request, jsonify
from models import Task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os  # Added for environment variable usage

task_routes = Blueprint('task_routes', __name__)

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/task_management')  # Updated to use environment variable
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def validate_task_data(data):
    """Validate incoming task data."""
    if not all(key in data for key in ("title", "priority")):
        return False, "Missing required fields"
    if data.get("priority") not in [e.value for e in TaskPriority]:
        return False, "Invalid priority value"
    return True, ""

@task_routes.route('/tasks', methods=['POST'])
def create_task():
    with Session() as session:  # Using context manager for session
        data = request.json
        is_valid, message = validate_task_data(data)
        if not is_valid:
            return jsonify({"message": message}), 400

        new_task = Task(**data)
        session.add(new_task)
        session.commit()
        return jsonify({"message": "Task created", "task_id": new_task.id}), 201

@task_routes.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    with Session() as session:  # Using context manager for session
        task = session.query(Task).filter(Task.id == id).first()
        if task:
            return jsonify({"id": task.id, "title": task.title, "status": task.status}), 200
        return jsonify({"message": "Task not found"}), 404

@task_routes.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    with Session() as session:  # Using context manager for session
        data = request.json
        task = session.query(Task).filter(Task.id == id).first()
        
        if task:
            is_valid, message = validate_task_data(data)
            if not is_valid:
                return jsonify({"message": message}), 400
            
            for key, value in data.items():
                if key in ['status', 'priority'] and value not in [e.value for e in TaskStatus] + [e.value for e in TaskPriority]:  # Validation check
                    return jsonify({"message": f"Invalid value for {key}"}), 400
                setattr(task, key, value)
            session.commit()
            return jsonify({"message": "Task updated"}), 200
        return jsonify({"message": "Task not found"}), 404

@task_routes.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    with Session() as session:  # Using context manager for session
        task = session.query(Task).filter(Task.id == id).first()
        if task:
            session.delete(task)
            session.commit()
            return jsonify({"message": "Task deleted"}), 200
        return jsonify({"message": "Task not found"}), 404
```

### Updated Test Scripts

**task_management_service/test/test_routes.py**
```python
import unittest
import json
from app import app

class TaskManagementServiceTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_task(self):
        response = self.app.post('/tasks', json={
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "High"  # Ensure priority is valid
        })
        self.assertEqual(response.status_code, 201)

    def test_create_task_missing_fields(self):
        response = self.app.post('/tasks', json={
            "description": "This is a test task"
        })
        self.assertEqual(response.status_code, 400)  # Check for missing fields

    def test_create_task_invalid_priority(self):
        response = self.app.post('/tasks', json={
            "title": "Test Task",
            "description": "This is a test task",
            "priority": "Invalid Priority"  # Invalid priority
        })
        self.assertEqual(response.status_code, 400)  # Check for invalid priority

    def test_get_task(self):
        response = self.app.get('/tasks/1')
        self.assertEqual(response.status_code, 200)

    def test_update_task(self):
        response = self.app.put('/tasks/1', json={"status": "In Progress"})
        self.assertEqual(response.status_code, 200)

    def test_update_task_invalid_status(self):
        response = self.app.put('/tasks/1', json={"status": "Invalid Status"})
        self.assertEqual(response.status_code, 400)  # Check for invalid status

    def test_delete_task(self):
        response = self.app.delete('/tasks/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

**notification_service/app.py**
```python
from flask import Flask, request, jsonify
import os  # Added for environment variable usage

app = Flask(__name__)

@app.route('/notifications', methods=['POST'])
def send_notification():
    data = request.json
    # Logic to send notification (email or in-app)
    return jsonify({"message": "Notification sent"}), 201

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 8080)))  # Updated to use environment variable for port
```

**reporting_service/app.py**
```python
from flask import Flask, jsonify
import os  # Added for environment variable usage

app = Flask(__name__)

@app.route('/reports', methods=['GET'])
def generate_report():
    # Logic to generate report (placeholder)
    return jsonify({"message": "Report generated"}), 200

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 8080)))  # Updated to use environment variable for port
```

### Updated README Files

**task_management_service/README.md**
```markdown
# Task Management Service

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up PostgreSQL database and create the `tasks` table.

3. Set the environment variable for the database URL:
   ```bash
   export DATABASE_URL='postgresql://user:password@localhost:5432/task_management'
   ```

4. Optionally, set the port environment variable:
   ```bash
   export PORT=8080
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. The service will be available at `http://localhost:8080`.
```

**notification_service/README.md**
```markdown
# Notification Service

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables for any sensitive information.

3. Optionally, set the port environment variable:
   ```bash
   export PORT=8080
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. The service will be available at `http://localhost:8080`.
```

**reporting_service/README.md**
```markdown
# Reporting Service

## Setup Instructions

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables for any sensitive information.

3. Optionally, set the port environment variable:
   ```bash
   export PORT=8080
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. The service will be available at `http://localhost:8080`.
```

### Conclusion
The codebase has been updated to incorporate all feedback from the code review. Key changes include:
- Proper relative imports.
- Use of environment variables for sensitive information and port configuration.
- Context management for database sessions.
- Refactored validation logic into a separate function for better readability.
- Enhanced error handling for invalid data.
- Updated test cases to cover edge cases and validation scenarios.

All sections of the codebase have been preserved as required, ensuring that the new version is an enhancement of the previous version.
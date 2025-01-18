from flask import Blueprint, request, jsonify
from models import Task, db

task_routes = Blueprint('task_routes', __name__)

@task_routes.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        status=data['status'],
        priority=data.get('priority'),
        due_date=data.get('due_date'),
        assignee_id=data.get('assignee_id')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created", "task": new_task.id}), 201

@task_routes.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify({"id": task.id, "title": task.title, "description": task.description, "status": task.status})

@task_routes.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    task.due_date = data.get('due_date', task.due_date)
    db.session.commit()
    return jsonify({"message": "Task updated"})

@task_routes.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
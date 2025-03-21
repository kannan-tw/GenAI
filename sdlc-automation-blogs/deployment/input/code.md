# Code Repository Structure

```
repo/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── providers.tf
├── ansible/
│   ├── inventory.ini
│   ├── playbook.yml
├── app/
│   ├── src/
│   │   ├── app.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── templates/
│   │       ├── index.html
│   │       ├── add_task.html
│   │       └── task_list.html
│   ├── config/
│   ├── Dockerfile
│   └── requirements.txt
└── docs/
    ├── SRS.md
    ├── HLD.md
    └── README.md
```

# Sample Task Management App Code

## `app.py`
```python
from flask import Flask, render_template, request, redirect
from database import init_db, add_task, get_tasks

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    tasks = get_tasks()
    return render_template('task_list.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    add_task(task)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## `database.py`
```python
import sqlite3

def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()

def add_task(name):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = c.fetchall()
    conn.close()
    return tasks
```

## `templates/task_list.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Task List</title>
</head>
<body>
    <h1>Task List</h1>
    <form action="/add" method="post">
        <input type="text" name="task" required>
        <button type="submit">Add Task</button>
    </form>
    <ul>
        {% for task in tasks %}
            <li>{{ task[1] }}</li>
        {% endfor %}
    </ul>
</body>
</html>
```
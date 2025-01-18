from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/task_db'
db = SQLAlchemy(app)

@app.route('/reports', methods=['GET'])
def generate_report():
    # Logic to generate report
    return jsonify({"message": "Report generated"}), 200

if __name__ == '__main__':
    app.run(port=8080)
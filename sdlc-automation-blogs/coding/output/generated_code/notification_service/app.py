from flask import Flask, request, jsonify
import pika

app = Flask(__name__)

@app.route('/notifications', methods=['POST'])
def send_notification():
    data = request.get_json()
    # Logic to send notification (e.g., email, in-app)
    return jsonify({"message": "Notification sent"}), 201

if __name__ == '__main__':
    app.run(port=8080)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive-message', methods=['POST'])
def receive_message():
    data = request.json
    message = data.get('message')
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    # Log the received message (prints to the console)
    print(f"Received Message: {message}")
    
    # Return a success message with the received message
    return jsonify({"status": "success", "received_message": message}), 200

@app.route('/receive-sql', methods=['POST'])
def receive_sql():
    data = request.get_json()
    sql_code = data.get('sql_code', '')
    print("Received SQL code:", sql_code)
    # Do something with the SQL code, like executing it or storing it
    return jsonify({"status": "success", "message": "SQL code received"}), 200


if __name__ == '__main__':
    app.run(debug=True)

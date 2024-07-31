from flask import Flask, request, jsonify

app = Flask(__name__)

""" @app.route('/execute-sql', methods=['POST'])
def execute_sql():
    data = request.json
    sql_query = data.get('sql_query')
    
    if not sql_query:
        return jsonify({"error": "No SQL query provided"}), 400
    
    # Log the received SQL query (prints to the console)
    print(f"Received SQL Query: {sql_query}")
    
    # Return a success message with the received query
    return jsonify({"status": "success", "received_query": sql_query}), 200 """

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

if __name__ == '__main__':
    app.run(debug=True)

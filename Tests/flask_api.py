from flask import Flask, request, jsonify
from connection_database import connect_to_mysql, execute_sql_query

app = Flask(__name__)

# Connect to the database
engine = connect_to_mysql()

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
    
    if not sql_code.strip():
        return jsonify({"error": "No SQL code provided"}), 400

    # Execute the SQL code and fetch results
    if engine:
        try:
            query_results = execute_sql_query(engine, sql_code)
            return jsonify({"status": "success", "results": query_results}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "Database connection failed"}), 500
    


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify

app = Flask(__name__)

# Standard Flask routes
@app.route('/')
def index():
    return jsonify({"status": "success", "message": "Hello Boys."}), 200

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    # Process the data as needed
    print(f"Received data via HTTP: {data}")
    return jsonify({"status": "success", "message": "Data received"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

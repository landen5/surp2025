from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/data", methods=["POST"])
def receive_data():
    
    data = request.json
    print("Received data:", data)  
    
    return jsonify({
        "status": "success",
        "message": "Data received successfully",
        "received_data": data
    })

if __name__ == "__main__":
    # Run the app on all network interfaces (0.0.0.0) to make it accessible from other devices
    app.run(host="0.0.0.0", port=8000, debug=True)
from flask import Flask, request, jsonify
from geocoder import geocode_address

app = Flask(__name__)

@app.route("/geocode", methods=["POST"])
def geocode():
    body = request.get_json()

    if not body or "address" not in body:
        return jsonify({"error": "Address is required"}), 400

    address = body["address"]

    result = geocode_address(address)
    if not result:
        return jsonify({"error": "Unable to geocode address"}), 404

    return jsonify(result), 200


@app.route("/", methods=["GET"])
def home():
    return {"message": "Flask Geocoder API is running"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

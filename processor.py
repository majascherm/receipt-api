from flask import Flask, jsonify, request
import uuid
import os
import math
import json

# Initialize the Flask application
app = Flask(__name__)

RECEIPTS_DIR = './receipts'
os.makedirs(RECEIPTS_DIR, exist_ok=True)

@app.route('/receipts/process', methods=['POST'])
def post_receipt():
    try:
        # Get JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON payload"}), 400

        # Generate a unique ID for the receipt
        receipt_id = str(uuid.uuid4())
        data["id"] = receipt_id

        # Save the JSON data to a file
        file_path = os.path.join(RECEIPTS_DIR, f"{receipt_id}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        return jsonify({"message": "Receipt saved", "id": receipt_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # Endpoint to get points for a receipt by ID
@app.route('/receipts/<id>/points', methods=['GET'])
def get_receipt_points(id):
    try:
        file_path = os.path.join(RECEIPTS_DIR, f"{id}.json")

        # Check if the receipt file exists
        if not os.path.exists(file_path):
            return jsonify({"error": "Receipt not found"}), 404

        # Load the receipt data
        with open(file_path, 'r') as f:
            receipt_data = json.load(f)

        # Calculate points 
        points = 0
        #Rules:
        # One point for every alphanumeric character in the retailer name.
        formatted_name = receipt_data["retailer"].strip()
        formatted_name = ''.join(char for char in formatted_name if char.isalnum())
        points = points + len(formatted_name)

        # 50 points if the total is a round dollar amount with no cents.
        # 25 points if the total is a multiple of 0.25.
        total = float(receipt_data["total"])
        if total % 1 == 0.0:
            points = points + 50
        if total % 0.25 == 0.0:
            points = points + 25

        # 5 points for every two items on the receipt.
        items = receipt_data.get("items")
        pairs = math.floor(len(items) / 2)
        points = points + (pairs*5)

        # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
        for item in items:
            description = item["shortDescription"].strip()
            if len(description) % 3 == 0:
                manipulated_price = float(item["price"]) * .2
                points = points + math.ceil(manipulated_price)
        # 6 points if the day in the purchase date is odd.
        day = int(receipt_data["purchaseDate"].split('-')[-1])
        if day % 2 == 1:
            points = points + 6
        # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        hour = int(receipt_data["purchaseTime"].split(':')[0])
        if hour >= 14 and hour < 16:
            points = points + 10

    
        return jsonify({"points": points})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
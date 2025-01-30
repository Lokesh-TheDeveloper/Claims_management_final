from flask import Flask, request, jsonify
from pymongo import MongoClient

# Initialize Flask App
app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Update with your actual MongoDB URI
db = client["claims_db"]
claims_collection = db["claims"]

# Policy Model
class Policy:
    def __init__(self, policy_id, policyholder, coverage_amount):
        self.policy_id = policy_id
        self.policyholder = policyholder
        self.coverage_amount = coverage_amount

# CRUD Operations using MongoDB
class ClaimsManager:
    def create_claim(self, claim_id, policy_id, amount, policy):
        if amount > policy.coverage_amount:
            return "Claim amount exceeds policy coverage!"
        
        claim_data = {
            "claim_id": claim_id,
            "policy_id": policy_id,
            "amount": amount,
            "status": "Pending"
        }
        claims_collection.insert_one(claim_data)
        return f"Claim {claim_id} created!"

    def get_claim(self, claim_id):
        claim = claims_collection.find_one({"claim_id": claim_id}, {"_id": 0})
        return claim if claim else "Claim not found"

    def update_claim(self, claim_id, new_status):
        result = claims_collection.update_one({"claim_id": claim_id}, {"$set": {"status": new_status}})
        return f"Claim {claim_id} updated!" if result.modified_count > 0 else "Claim not found"

    def delete_claim(self, claim_id):
        result = claims_collection.delete_one({"claim_id": claim_id})
        return f"Claim {claim_id} deleted!" if result.deleted_count > 0 else "Claim not found"

# Initialize ClaimsManager
claims_manager = ClaimsManager()

# API Endpoints
@app.route("/claim", methods=["POST"])
def create_claim():
    data = request.json
    policy = Policy(data["policy_id"], "John Doe", 10000)  # Example policy
    
    # Check if claim already exists
    if claims_collection.find_one({"claim_id": data["claim_id"]}):
        return jsonify({"error": "Claim ID already exists!"}), 400
    
    response = claims_manager.create_claim(data["claim_id"], data["policy_id"], data["amount"], policy)
    return jsonify({"message": response})

@app.route("/claim/<int:claim_id>", methods=["GET"])
def get_claim(claim_id):
    claim = claims_manager.get_claim(claim_id)
    return jsonify({"claim": claim}) if claim != "Claim not found" else (jsonify({"error": "Claim not found"}), 404)

@app.route("/claim/<int:claim_id>", methods=["PUT"])
def update_claim(claim_id):
    data = request.json
    response = claims_manager.update_claim(claim_id, data["status"])
    return jsonify({"message": response})

@app.route("/claim/<int:claim_id>", methods=["DELETE"])
def delete_claim(claim_id):
    response = claims_manager.delete_claim(claim_id)
    return jsonify({"message": response})

if __name__ == "__main__":
    app.run(debug=True)

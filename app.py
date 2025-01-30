from flask import Flask, request, jsonify
from flasgger import Swagger
from pymongo import MongoClient

# Initialize Flask App
app = Flask(__name__)
Swagger(app)

# API Key (Use an environment variable in production)
API_KEY = "1122c939bfdfb36e64f5aa125d0a57f70404fcfd09a5069213e8465762d69b65"

# Connect to MongoDB
client = MongoClient("mongodb+srv://lokeshkumawat1903:lokeshjojo@claimscluster.r2ikn.mongodb.net/?retryWrites=true&w=majority&appName=ClaimsCluster")  
db = client["claims_db"]
claims_collection = db["claims"]

# Middleware to verify API key
def verify_api_key():
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized - Invalid API key"}), 401
    return None  # No error means the key is valid

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

# API Endpoints with API Key Authentication
@app.route("/claim", methods=["POST"])
def create_claim():
    auth_error = verify_api_key()
    if auth_error: return auth_error  # Unauthorized access

    data = request.json
    policy = Policy(data["policy_id"], "John Doe", 10000)  # Example policy
    
    if claims_collection.find_one({"claim_id": data["claim_id"]}):
        return jsonify({"error": "Claim ID already exists!"}), 400
    
    response = claims_manager.create_claim(data["claim_id"], data["policy_id"], data["amount"], policy)
    return jsonify({"message": response})

@app.route("/claim/<int:claim_id>", methods=["GET"])
def get_claim(claim_id):
    auth_error = verify_api_key()
    if auth_error: return auth_error  # Unauthorized access

    claim = claims_manager.get_claim(claim_id)
    return jsonify({"claim": claim}) if claim != "Claim not found" else (jsonify({"error": "Claim not found"}), 404)

@app.route("/claim/<int:claim_id>", methods=["PUT"])
def update_claim(claim_id):
    auth_error = verify_api_key()
    if auth_error: return auth_error  # Unauthorized access

    data = request.json
    response = claims_manager.update_claim(claim_id, data["status"])
    return jsonify({"message": response})

@app.route("/claim/<int:claim_id>", methods=["DELETE"])
def delete_claim(claim_id):
    auth_error = verify_api_key()
    if auth_error: return auth_error  # Unauthorized access

    response = claims_manager.delete_claim(claim_id)
    return jsonify({"message": response})

if __name__ == "__main__":
    app.run(debug=True)

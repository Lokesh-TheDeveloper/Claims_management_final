from flask import Flask, request, jsonify
from flasgger import Swagger    # flasgger is used for generating Swagger UI at default location /apidocs
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId



# Initialize Flask App
app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/claim*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE"]}})

Swagger(app)  # Initialize Swagger

# Connect to MongoDB
client = MongoClient("mongodb+srv://lokeshkumawat1903:lokeshjojo@claimscluster.r2ikn.mongodb.net/?retryWrites=true&w=majority&appName=ClaimsCluster")  

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
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data received"}), 400
        
         # Console log the received data
        # print("Received data from frontend:", data)

        # Extract data
        claim_id = data.get("claim_id")
        policy_id = data.get("policy_id")
        amount = data.get("amount")

        if not claim_id or not policy_id or not amount:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Check if the claim ID already exists in MongoDB
        if claims_collection.find_one({"claim_id": claim_id}):
            return jsonify({"error": "Claim ID already exists!"}), 400

        # Create claim data
        claim_data = {
            "claim_id": claim_id,
            "policy_id": policy_id,
            "amount": amount,
            "status": "Pending"
        }

        # Insert into MongoDB
        claims_collection.insert_one(claim_data)

        # Normally, you would save this in a database (mock response)
        return jsonify({"message": "Claim created successfully!", "claim": data}), 201

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Internal Server Error"}), 500




#  changess 


# @app.route("/claim", methods=["POST"])
# def create_claim():
#     """
#     Create a new insurance claim
#     ---
#     parameters:
#       - name: claim_id
#         in: body
#         type: integer
#         required: true
#         description: The unique identifier for the claim
#       - name: policy_id
#         in: body
#         type: string
#         required: true
#         description: The unique identifier for the policy
#       - name: amount
#         in: body
#         type: float
#         required: true
#         description: The amount of the claim
#     responses:
#       200:
#         description: Claim created successfully
#         schema:
#           type: object
#           properties:
#             message:
#               type: string
#               example: "Claim 101 created!"
#       400:
#         description: Claim ID already exists
#     """
#     data = request.json
    
#     policy = Policy(data["policy_id"], "John Doe", 10000)  # Example policy
    
#     # Check if claim already exists
#     if claims_collection.find_one({"claim_id": data["claim_id"]}):
#         return jsonify({"error": "Claim ID already exists!"}), 400
    
#     response = claims_manager.create_claim(data["claim_id"], data["policy_id"], data["amount"], policy)
#     return jsonify({"message": response})

@app.route("/claim/<int:claim_id>", methods=["GET"])
def get_claim(claim_id):
    """
    Get a claim by ID
    ---
    parameters:
      - name: claim_id
        in: path
        type: integer
        required: true
        description: The unique identifier for the claim
    responses:
      200:
        description: Claim details
        schema:
          type: object
          properties:
            claim_id:
              type: integer
              example: 101
            policy_id:
              type: string
              example: "POLICY123"
            amount:
              type: float
              example: 1500.0
            status:
              type: string
              example: "Pending"
      404:
        description: Claim not found
    """
    claim = claims_manager.get_claim(claim_id)
    return jsonify({"claim": claim}) if claim != "Claim not found" else (jsonify({"error": "Claim not found"}), 404)


@app.route("/claim-list", methods=["GET"])
def get_all_claims():
    """
    Get all claims
    ---
    responses:
      200:
        description: List of all claims
    """
    claims = list(claims_collection.find({}, {"_id": 0}))  # Retrieve all claims from MongoDB
    return jsonify({"claims": claims})



@app.route("/claim/<int:claim_id>", methods=["PUT"])
def update_claim(claim_id):
    """
    Update claim status
    ---
    parameters:
      - name: claim_id
        in: path
        type: integer
        required: true
        description: The unique identifier for the claim
      - name: status
        in: body
        type: string
        required: true
        description: The new status for the claim
    responses:
      200:
        description: Claim updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Claim 101 updated!"
      404:
        description: Claim not found
    """
    data = request.json
    response = claims_manager.update_claim(claim_id, data["status"])
    return jsonify({"message": response})

@app.route("/claim/<int:claim_id>", methods=["DELETE"])
def delete_claim(claim_id):
    # """
    # Delete a claim
    # ---
    # parameters:
    #   - name: claim_id
    #     in: path
    #     type: integer
    #     required: true
    #     description: The unique identifier for the claim
    # responses:
    #   200:
    #     description: Claim deleted successfully
    #     schema:
    #       type: object
    #       properties:
    #         message:
    #           type: string
    #           example: "Claim 101 deleted!"
    #   404:
    #     description: Claim not found
    # """
    print(f"Attempting to delete claim with ID: {claim_id}")  # Check claim_id
    try:
        result = claims_collection.delete_one({"claim_id": str(claim_id)})  # Assuming the claim ID is _id in MongoDB
        if result.deleted_count > 0:
            return jsonify({"message": "Claim deleted successfully."}), 200
        else:
            return jsonify({"error": "Claim not found."}), 404
    except Exception as e:
        print("Error during deletion:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
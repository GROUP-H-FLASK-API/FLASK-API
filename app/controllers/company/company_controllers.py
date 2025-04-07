from flask import Blueprint, request, jsonify

company_bp = Blueprint("company", __name__)

# Sample in-memory database
companies = []

# Create a company
@company_bp.route("/", methods=["POST"])
def create_company():
    data = request.get_json()
    company = {"id": len(companies) + 1, "name": data["name"], "industry": data["industry"]}
    companies.append(company)
    return jsonify(company), 201

# Get all companies
@company_bp.route("/", methods=["GET"])
def get_companies():
    return jsonify(companies)

# Get a single company by ID
@company_bp.route("/<int:company_id>", methods=["GET"])
def get_company(company_id):
    company = next((c for c in companies if c["id"] == company_id), None)
    return jsonify(company) if company else ("Company not found", 404)

# Update a company
@company_bp.route("/<int:company_id>", methods=["PUT"])
def update_company(company_id):
    data = request.get_json()
    company = next((c for c in companies if c["id"] == company_id), None)
    if company:
        company.update(data)
        return jsonify(company)
    return ("Company not found", 404)

# Delete a company
@company_bp.route("/<int:company_id>", methods=["DELETE"])
def delete_company(company_id):
    global companies
    companies = [c for c in companies if c["id"] != company_id]
    return ("", 204)

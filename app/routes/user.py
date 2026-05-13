from flask import Blueprint, jsonify, request

users_bp = Blueprint("users", __name__)

users = []


# --------------------
# GET ALL USERS
# --------------------
@users_bp.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200


# --------------------
# CREATE USER
# --------------------
@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    required_fields = ["username", "email", "password"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    new_user = {
        "id": len(users) + 1,
        "username": data["username"],
        "email": data["email"],
        "password": data["password"]
    }

    users.append(new_user)

    return jsonify({
        "message": "User created successfully",
        "user": new_user
    }), 201


# --------------------
# GET USER BY ID
# --------------------
@users_bp.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    for user in users:
        if user["id"] == id:
            return jsonify(user), 200

    return jsonify({"error": "User not found"}), 404


# --------------------
# UPDATE USER
# --------------------
@users_bp.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    for user in users:
        if user["id"] == id:
            user["username"] = data.get("username", user["username"])
            user["email"] = data.get("email", user["email"])
            user["password"] = data.get("password", user["password"])

            return jsonify({
                "message": "User updated successfully",
                "user": user
            }), 200

    return jsonify({"error": "User not found"}), 404


# --------------------
# DELETE USER
# --------------------
@users_bp.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    for user in users:
        if user["id"] == id:
            users.remove(user)
            return jsonify({"message": "User deleted successfully"}), 200

    return jsonify({"error": "User not found"}), 404
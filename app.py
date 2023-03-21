import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/api/users/")
def get_users():
    """
    Endpoint for getting all users
    """
    return json.dumps({"users": DB.get_all_users()}), 200

@app.route("/api/users/", methods = ["POST"])
def create_user():
    """
    Endpoint for creating a new user
    """

    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    balance = body.get("balance")
    
    user_id = DB.insert_users_table(name, username, balance)
    user = DB.get_users_by_id(user_id)

    if user is None:
        return json.dumps({"error": "Something went wrong while making the user"}), 404
    return json.dumps(user), 201

@app.route("/api/user/<int:user_id>/")
def get_user(user_id):
    """
    Endpoint for getting a user by ID
    """

    user = DB.get_users_by_id(user_id)
    if user is None:
        return json.dumps({"error": "User is not found!"}), 404
    return json.dumps(user), 200

@app.route("/api/user/<int:user_id>/", methods=["DELETE"])
def delete_user(user_id):
    """
    Endpoint for deleting user by ID
    """
    user = DB.get_users_by_id(user_id)

    if user is None:
        return json.dumps({"error": "User not found!"}), 404

    DB.delete_user_by_id(user_id)
    return json.dumps(user), 200

@app.route("/api/send/", methods=["POST"])
def send_money():
    """
    Endpoint for sending money from one user to another
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    reciever_id = body.get("receiver_id")
    amount = body.get("amount")

    sender = DB.get_users_by_id(sender_id)

    if sender is None:
        return json.dumps({"error": "Sender not found!"}), 404
    
    reciever = DB.get_users_by_id(reciever_id)

    if reciever is None:
        return json.dumps({"error": "Reciever not found!"}), 404
    
    is_one = DB.send_money(sender_id, reciever_id, amount)
    if is_one == 0:
        return json.dumps({"error": "Sender has too little money to send this amount!"}), 400
    return json.dumps({"sender_id": sender_id, "receiver_id": reciever_id, "amount": amount}), 200



# your routes here


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

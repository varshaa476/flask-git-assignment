from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import json
import os
import certifi

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://varshaprabhudev03_db_user:MQIEXuiuZZEvFiop@cluster0.7nghuwf.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), tlsDisableOCSPEndpointCheck=True)
db = client["myapp_db"]
collection = db["submissions"]


@app.route("/api", methods=["GET"])
def get_data():
    file_path = os.path.join(os.path.dirname(__file__), "data.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return jsonify(data)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form.get("name")
        email = request.form.get("email")

        if not name or not email:
            return render_template("index.html", error="Name and Email are required.")

        collection.insert_one({"name": name, "email": email})
        return redirect(url_for("success"))

    except Exception as e:
        return render_template("index.html", error=str(e))


@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    try:
        item_name = request.form.get("itemName")
        item_description = request.form.get("itemDescription")

        if not item_name or not item_description:
            return jsonify({"error": "itemName and itemDescription are required"}), 400

        todo_collection = db["todos"]
        todo_collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description
        })

        return jsonify({"message": "To-do item added successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))

db = client["todo_database"]
collection = db["todo_items"]


@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():

    data = request.get_json()

    itemName = data.get("itemName")
    itemDescription = data.get("itemDescription")

    todo = {
        "itemName": itemName,
        "itemDescription": itemDescription
    }

    collection.insert_one(todo)

    return jsonify({
        "message": "To-Do item submitted successfully"
    }), 201


if __name__ == '__main__':
    app.run(debug=True)

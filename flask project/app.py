
from flask import Flask, request, render_template, redirect, url_for, jsonify
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is missing from .env")

# MongoDB connection
client = MongoClient(
    MONGO_URI,
    server_api=ServerApi("1"),
    serverSelectionTimeoutMS=5000
)

db = client.test
collection = db.entries

app = Flask(__name__)


# Home page
@app.route("/")
def home():
    day = datetime.today().strftime("%A")
    return render_template("index.html", day=day)


# Submit form
@app.route("/submit", methods=["POST"])
def submit():
    form_data = dict(request.form)

    try:
        collection.insert_one(form_data)
        print("Data inserted successfully")
        return redirect(url_for("success"))

    except Exception as e:
        print("Error:", e)

        return render_template(
            "index.html",
            day=datetime.today().strftime("%A"),
            error="Failed to submit data. Please try again."
        ), 500


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


# View stored data
@app.route("/view")
def view():
    try:
        data = list(collection.find({}, {"_id": 0}))
        return jsonify({"data": data})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Unable to fetch data"}), 500


if __name__ == "__main__":
    app.run(debug=True)

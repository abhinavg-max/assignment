from flask import Flask, jsonify
import json
import os

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_FILE = os.path.join(BASE_DIR, 'data.json')


@app.route('/api')
def get_data():
    with open(JSON_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
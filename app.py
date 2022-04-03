from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/")
def endpoint():
    return jsonify({"meta": {"message": "Hello World"}})
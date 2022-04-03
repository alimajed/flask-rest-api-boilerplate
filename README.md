# flask-rest-api-boilerplate
this is a simple project can be used as a **boilerplate** of rest api projects using flask

## Create simple REST API endpoint
* create file ***app.py** and past this code into it
    ```
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route("/api/")
    def endpoint():
        return jsonify({"meta": {"message": "Hello World"}})
    ```
* to run the app, first you need to export multiple variables, so open your terminal
    * ```export FLASK_ENV=development```
    * ```export FLASK_APP=app```
* run the app 
    * ```flask run```
* this is our first step
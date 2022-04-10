# flask-rest-api-boilerplate
this is a simple project that can be used as a **boilerplate** of the rest API projects using flask

## Create a Simple REST API endpoint
* create file ***app.py** and paste this code into it
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
* This is our first step

## Dockerize Flask App
* create file **Dockerfile** and paste this code into it
    ```
    FROM python:3.10.4-alpine

    RUN mkdir /app
    WORKDIR /app

    COPY ./requirements.txt requirements.txt
    RUN pip install -r requirements.txt
    COPY . .

    RUN addgroup -S appgroup && adduser -S appuser -G appgroup
    USER appuser

    EXPOSE 5000

    RUN ls -ln

    ENTRYPOINT ["sh", "/app/start.sh" ]
    ```
    * **WORKDIR** command is to tell Docker the default app directory and no need to specify it in other commands, only put **.**
    * **COPY** command to copy files from source to destination
    * **RUN** run any command after it
    * **USER** choose the default user for the image
    * **ENTRYPOINT** specify the entry point of the container once it is up
* to build the image, run
    ```
    docker build . -t flask
    ```
    * *-t* tag the image, so we can call it by its tag name
* to run the container (image instance), run
    ```
    docker run --rm -it -p 5000:5000 -v "%cd%":/app flask
    ```
    * *--rm* means remove the container after it stops
    * *-p* publish ports "host:container"
    * *-v* bind mount a volume

## Docker Compose
* Compose is a tool for defining and running multi-container Docker applications
* Now we have only one container, it may not make much difference
* but yet, in the **docker-compose.yml** file we will create we can put variables and volumes in a way to simplify **Dockerfile** and the command *docker run*, especially when our app will expand in the coming steps
* create **docker-compose.yml** file and paste this code into it
    ```
    version: "3.9"

    services:
    flask:
        build: .
        container_name: flask
        ports:
        - "5000:5000"
        volumes:
        - .:/app
    ```
* as we see, this file can contain the needed configuration
* to build the image, run
    ```
    docker-compose build
    ```
* to run the container, run
    ```
    docker-compose up
    ```
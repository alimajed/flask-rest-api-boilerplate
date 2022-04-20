# flask-rest-api-boilerplate
this is a simple project that can be used as a **boilerplate** of the rest API projects using [flask](https://flask.palletsprojects.com/en/2.1.x/)

<br><br>

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

<br>

## [Dockerize Flask App](https://www.docker.com/)
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

<br>

## [Docker Compose](https://docs.docker.com/compose/)
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

<br>

## [Application Factory Pattern](https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/)
* an enterprise flask application needs multiple configuration environments, many blueprints (modules) to be registered, adding databases and other packages
* using the simple flask application to init the app might not be the best solution
* here comes the factory pattern
    * the app can modularized and organized
    * easy setup to handle multiple environments

<br>

## Implementing Application Factory Pattern
* create a folder **app** with a file **__init__.py** in it
* this init file will contain ***init_app*** or ***create_app***
* inside this function we will handle blueprints (and other packages) registration
* after the setup is done, the function will return the ***app*** object
* simple application factory will look like this
    ```
    from flask import Flask

    from config import ConfigFactory


    def init_app():
        app = Flask(__name__)
        app.config.from_object(ConfigFactory.factory().__class__)

        with app.app_context():
            # import blueprints
            from app.home.views import home_bp

            # register blueprints
            app.register_blueprint(home_bp, url_prefix="/api/home")

            return app
    ```
* in the project root we will create **config.py** and it will be our config factory
* the config factory will load the configuration of which environment we want to run
* passing an argument to **FLASK_APP** or defining a **FLASK_ENV** will help
* the code inside the config factory will look like
    ```
    from os import getenv


    class ConfigFactory:
        def factory():
            env = getenv("FLASK_ENV", "development")

            if env in ["development"]:
                return Development()

        factory = staticmethod(factory)


    class Config:
        """base config class contains common configurations in all environments"""
        pass

    class Development(Config):
        DEBUG = True
        TESTING = False
    ```
    * the config factory has a base config class containing all common configurations between the environment
    * we can add class as much as we have a different environment, by inheriting from the base config class

<br>

## Database and Docker for Development
* before heading to implement the database part, let's talk about the main feature of this project
* this project offers a 100% docker for the development environment
* you don't need to download and install any database server or database management tools or any other tools (like Redis for example)
* you only need docker to be installed on your machine and run 2 commands to make your environment ready
    * `docker-compose build`
    * `docker-compose up`
* in this project we are using only alpine images because it is the most lightweight images

<br>

## Adding Postgres
* to add postgres database to our environment, we need to create a new image (service) in our docker-compose file
    ```
    postgres:
        image: postgres:alpine
        container_name: postgres
        networks:
            - default
        env_file:
        - ./.envs/postgres.env
        ports:
            - 5432:5432
        restart: on-failure:5
        volumes:
            - postgres_data:/var/lib/postgresql/data
    ```
    * we are using the official postgres alpine image, but we can build our custom image via a new docker file for postgres image
    * load the environment variables for postgres image via a file ***./.envs/postgres.env*** using **env_file** keyword
* we need to create a volume object for postgres data, so put it under volumes
    ```
    volumes:
        pgadmin_data: {}
    ```

<br>

## Adding PGAdmin
* to add postgres database to our environment, we need to create a new image (service) in our docker compose file
    ```
    pg-admin:
        image: dpage/pgadmin4
        container_name: pgadmin
        networks:
            - default
        env_file:
        - ./.envs/pgadmin.env
        ports:
            - 5050:80
        logging:
        driver: none
        restart: on-failure:5
    ```
    * we are using the official pgadmin alpine image, but we can build our custom image via a new docker file for pgadmin image
    * load the environment variables for pgadmin image via a file ***./.envs/pgadmin.env*** using **env_file** keyword
* we need to create a volume object for pgadmin data, so put it under volumes
    ```
    volumes:
        pgadmin_data: {}
    ```

<br>

## Adding Database Required Packages
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) is a Flask extension that adds support to [SQLAlchemy](https://www.sqlalchemy.org/) the best common ORM used in Flask application
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is a flask extension to handle database migrations
* since we are using the PostgreSQL database, [Psycopg2](https://www.psycopg.org/) is the most popular PostgreSQL database adapter for the Python programming language

## Dockerfile modifications
* some packages are required to be installed on the image to build **psycopg2**
* we add the following to the **Dockerfile**
    ```
    # add packages for psycopg2
    RUN apk update && apk upgrade
    # RUN apk add --no-cache libpq-dev gcc
    RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
    ```

## Adding Database Configuration
* we have created a new ***database.py*** in the app directory that will contain the database configuration
* we import flask-sqlalchemy and flask-migrate installed package to **__init__.py** file and we initialize them
    ```
    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ```
* **DATABASE_URI** variable need to be exported so that the flask app will connect to the database
    ```
    export DATABASE_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
    ```
* sqlalchemy will search by default for a variable called **SQLALCHEMY_DATABASE_URI**, so we add this variable to **config.py**
    ```
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")
    ```

## Adding User Module
* we mentioned above that the factory pattern helps to modularize the application structure
* the ***app*** directory will conatains different coded modules of the project
* we assume that each module/package will be registered to a blueprint and contains such files like
    * **views.py**
    * **models.py**
* first we create the **common module** that will contain code imported in different modules
    * inside this module we create **db_model_base.py** containing the abstract base model inherited from SQLalchemy DB model
        ```
        class BaseModel(db.Model):
            __abstract__ = True

            id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
            created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone("UTC")))
            updated_at = db.Column(db.DateTime(timezone=True), nullable=True)
        ```
    * flask-migrate will know that classes that inherit SQLalchemy DB model are database models (tables)
    * the base model contains the columns that we want to be in all our application database models
    * any new models in other modules should inherit this base model class
* we have created a new module/package **user** and we add the ***UserModel***
    ```
    class UserModel(BaseModel):
        __tablename__ = "user"

        first_name = Column(String(100), nullable=False)
        last_name = Column(String(100), nullable=False)
        date_of_birth = Column(Date, nullable=False)
        email = Column(String(100), nullable=False, unique=True)
        password = Column(String(300), nullable=False)
    ```

<br>

## Database Migrations
* to init database migrations process we run (only once)
    ```
    docker-compose run --rm flask flask db init
    ```
* this command will create ***migrations/*** folder that contains migrations files
* if the new changes to our database have new database models, we should import them inside **env.py** under
    ```
    # add your model's MetaData object here
    # for 'autogenerate' support
    # from myapp import mymodel
    from app.user.models import UserModel
    ```
* to collect new changes to be applied to our database we run
    ```
    docker-compose run --rm flask flask db migrate
    ```
* finally we update our **start.sh** entry-point file to run `flask db upgrade` once we run our application
    * this command will look for database changes not applied to the database and will apply them
    * the database then will have the latest changes (if exist)
[![CI](https://github.com/alimajed/flask-rest-api-boilerplate/actions/workflows/ci.yml/badge.svg)](https://github.com/alimajed/flask-rest-api-boilerplate/actions/workflows/ci.yml)

# flask-rest-api-boilerplate
* **this is a simple project that can be used as a boilerplate for the rest API projects using [flask](https://flask.palletsprojects.com/en/2.1.x/)**
* **we will use [application factory pattern]((https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/)) that helps to modularize project structure**
* **we will use [Docker](https://www.docker.com/) to create the environments for development and production, and it can be extended to as many environments you need (staging, UAT,...)**

<br><br>

## Application Factory Pattern
* an enterprise flask application needs multiple configuration environments, many blueprints (modules) to be registered, adding databases and other packages
* using the simple flask application to init the app might not be the best solution
* here comes the factory pattern
    * The app can be modularized and organized
    * easy setup to handle multiple environments

<br>

## Project Structure
* we mentioned above that the factory pattern helps to modularize the application structure
* the ***app*** directory will contain different coded modules of the project
* we assume that each module/package will be registered to a blueprint and contains such files like
    * **view.py** file contains the API routes
    * **schemas.py** contains the request serialization and deserialization
    * **models.py** contains the database models
    * **daos.py** *data access object* contains the business logic and this is the layer where we connect and fetch data to/from the database
    * **tests.py** contains the tests of the module
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
* for example, the project contains a module/package **user** and we add the ***UserModel*** that inherits form **BaseModel**
    ```
    class UserModel(BaseModel):
        __tablename__ = "user"

        first_name = Column(String(100), nullable=False)
        last_name = Column(String(100), nullable=False)
        sex = Column(String(100), nullable=False)
        date_of_birth = Column(Date, nullable=False)
        email = Column(String(100), nullable=False, unique=True)
        password = Column(String(300), nullable=False)
    ```

<br>

## Database and Docker for Development
* before heading to implement the database part, let's talk about the main feature of this project
* This project offers a 100% docker for the development environment
* you don't need to download and install any database server or database management tools or any other tools (like Redis for example)
* you only need docker to be installed on your machine and run 2 commands to make your environment ready
    * `docker-compose -f development.yml build`
    * `docker-compose -f development.yml up`
* in this project we are using only alpine images because it is the most lightweight images

<br>

## Adding Postgres
* to add postgres database to our environment, we need to create a new image (service) in our **docker-compose** development file
    ```
    postgres:
        image: postgres:alpine
        container_name: postgres
        networks:
            - default
        env_file:
        - ./.envs/.development/postgres.env
        ports:
            - 5432:5432
        restart: on-failure:5
        volumes:
            - postgres_data:/var/lib/postgresql/data
    ```
    * We are using the official postgres alpine image, but we can build our custom image via a new docker file for postgres image
    * load the environment variables for postgres image via a file ***./.envs/.development/postgres.env*** using **env_file** keyword
* We need to create a volume object for postgres data, so put it under volumes
    ```
    volumes:
        pgadmin_data: {}
    ```

<br>

## Adding PGAdmin
* to add the postgres database to our environment, we need to create a new image (service) in our **docker-compose** development file
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
    * We are using the official pgadmin alpine image, but we can build our custom image via a new docker file for pgadmin image
    * load the environment variables for pgadmin image via a file ***./.envs/.development/pgadmin.env*** using **env_file** keyword
* We need to create a volume object for pgadmin data, so put it under volumes
    ```
    volumes:
        pgadmin_data: {}
    ```

<br>



## Database Migrations
* to init database migrations process we run (only once)
    ```
    docker-compose -f development run --rm flask db init
    ```
* This command will create ***migrations/*** folder that contains migrations files
* if the new changes to our database have new database models, we should import them inside **env.py** under
    ```
    # add your model's MetaData object here
    # for 'autogenerate' support
    # from myapp import mymodel
    from app.user.models import UserModel
    ```
* to collect new changes to be applied to our database we run
    ```
    docker-compose run -f development --rm flask flask db migrate
    ```
* finally we update our **run-development.sh** (command) file to run `flask db upgrade` once we run our application
    * This command will look for database changes not applied to the database and will apply them
    * the database then will have the latest changes (if exist)

<br>

## Wait for Postgres
* in **docker-compose** development file we notice that service *flask* depends on *Postgres*
* in some cases, especially if we run the project for the first time or we run database migrations, the database could not be created yet, and *flask* service will throw an error
* **there is a difference between service Postgres is up and the required databases are created**
* in our project we have 2 databases, one for development and the other for testing, to isolate the testing environment
* let's say that our project depends on more than 2 databases, the time of creation will be longer, and putting a constant time to wait is not an ideal solution, it should be dynamic
* installing new packages in the *flask* service (image) like Postgres-client is also not preferable since we want to keep our image light-weight as much as we can
* here comes the **wait_for_postgres.py** that we call at an early stage during the initialization of the *flask* service (container) that check if the database (or the main one) is created, then we continue to process the entry point steps

<br>

## Docker for Production (and other envs)
* the **Dockerfile** contains the base image that we want our project to run on in the different environments
* since it is a boilerplate example, we will make only one additional production environment
* the **Dockerfile** will pass some parameters to prepare the image in the best way for the target environment
* inside **docker-compose** development and production files, we pass the parameters under arguments **args** option, for example for development we pass
    ```
    args:
        - BUILD_TARGET=development
        - TARGET_PORT=5000
        - COMMAND=run-development.sh
        - ENTRYPOINT=entrypoint-development.sh
    ```
* to build and run the image for any environment. just run the commands and specify the **docker-compose** file, like for production
    * `docker-compose -f development.yml build`
    * `docker-compose -f development.yml up`

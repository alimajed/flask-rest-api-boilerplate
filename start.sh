#!/bin/bash
export FLASK_ENV='development'
export FLASK_APP='app:init_app'

export POSTGRES_DB=$(echo $POSTGRES_MULTIPLE_DATABASES | cut -d, -f1)
export POSTGRES_TEST_DB=$(echo $POSTGRES_MULTIPLE_DATABASES | cut -d, -f2)

export DATABASE_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
export DATABASE_TEST_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_TEST_DB}"


python wait_for_postgres.py

if [ $# -eq 0 ]; then
    echo Starting App...
    flask db upgrade
    flask run -h 0.0.0.0 -p 5000
elif [ $1 == 'test' ]; then
    echo Test...
    export FLASK_ENV='testing'
    coverage run -m pytest -s
else
    exec "$@"
fi

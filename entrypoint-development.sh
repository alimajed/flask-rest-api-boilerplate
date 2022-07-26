#!/bin/bash
export FLASK_APP='app:init_app'

export POSTGRES_DB=$(echo $POSTGRES_MULTIPLE_DATABASES | cut -d, -f1)
export POSTGRES_TEST_DB=$(echo $POSTGRES_MULTIPLE_DATABASES | cut -d, -f2)

export DATABASE_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
export DATABASE_TEST_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_TEST_DB}"


for i in "$@"; do
    if [[ "$i" == "pytest" ]] ; then
        echo "Testing ..."
        export IS_TESTING="true"
        export TESTING=true
    fi
done

python wait_for_postgres.py

exec "$@"

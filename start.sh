#!/bin/bash
export FLASK_ENV=development
export FLASK_APP='app:init_app'
export DATABASE_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
echo ${DATABASE_URI}

if [ $# -eq 0 ]; then
    echo Starting App...
    flask db upgrade
    flask run -h 0.0.0.0 -p 5000
else
    exec "$@"
fi

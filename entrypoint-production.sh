#!/bin/bash
export FLASK_APP='app:init_app'

export DATABASE_URI="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}/${POSTGRES_DB}"

exec "$@"

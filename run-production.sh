#!/bin/bash
export FLASK_ENV='production'
export FLASK_APP='app:init_app'

export DATABASE_URI="postgresql://gqwtkdvo:z8LRprfT7ESxz2SZrMkSY14fGPQHHpTy@abul.db.elephantsql.com/gqwtkdvo"
# postgres://gqwtkdvo:z8LRprfT7ESxz2SZrMkSY14fGPQHHpTy@abul.db.elephantsql.com/gqwtkdvo
export JWT_SECRET_KEY="$3Cr3T"


flask db upgrade
# flask run -h 0.0.0.0 -p 5000

gunicorn -w 3 run:app

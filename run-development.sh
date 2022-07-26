#!/bin/bash

if [ $# -eq 0 ]; then
    echo Starting App...
    flask db upgrade
    flask run -h 0.0.0.0 -p 5000
else
    exec "$@"
fi

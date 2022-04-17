#!/bin/bash
export FLASK_ENV=development
export FLASK_APP='app:init_app'
flask run -h 0.0.0.0 -p 5000
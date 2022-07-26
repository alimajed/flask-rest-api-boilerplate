#!/bin/bash

flask db upgrade

gunicorn -w 3 run:app -b 0.0.0.0:8000

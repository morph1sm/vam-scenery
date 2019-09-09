#!/bin/bash

echo "Starting VAM Scenery Dev Server"

./venv/bin/activate
export FLASK_APP=scenery.py
export FLASK_DEBUG=1

flask run --host 0.0.0.0 --port=6969

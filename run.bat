REM @echo off
echo "Starting Local Scenery Server"
CALL venv\Scripts\activate
set FLASK_APP=scenery.py
set FLASK_DEBUG=1
py -m flask run --port=6969

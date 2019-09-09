#!/bin/bash
echo "Setting up VAM Scenery Flask App"

python -m venv venv
./venv/bin/activate
pip install --upgrade pip
pip install flask pyinstaller bigjson

echo " "
echo " "
echo "Type 'run', to run VAM Scenery in debug mode."
echo " "
echo "Type 'build', to make an executable."

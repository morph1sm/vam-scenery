
echo "Setting up VAM Scenery Flask App"
py -3 -m venv venv
CALL venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install flask pyinstaller bigjson

echo " "
echo " "
echo "Type 'run', to run VAM Scenery in debug mode."
echo " "
echo "Type 'build', to make an executable."

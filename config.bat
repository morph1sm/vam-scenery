
echo "Setting up Flask App"
py -3 -m venv venv
CALL venv\Scripts\activate
py -m pip install --upgrade pip
py -m pip install flask pyinstaller

echo "Type run, to run Scenery in debug mode."
echo "Type build, to make an executable. Then copy that to your VAM root folder and start it before running VAM."


echo "Building VAM Scenery Windows Executable"
CALL venv\Scripts\activate
pyinstaller --onefile --add-data "templates;templates" scenery.py

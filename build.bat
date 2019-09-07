
echo "Building Local Scenery Windows Executable"
CALL venv\Scripts\activate
pyinstaller --onefile --add-data "templates;templates" scenery.py
copy dist\scenery.exe \VAM

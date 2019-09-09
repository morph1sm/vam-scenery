
echo "Building VAM Scenery Windows Executable"
./venv/bin/activate
pyinstaller --onefile --add-data "templates:templates" scenery.py

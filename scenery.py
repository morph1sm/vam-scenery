import sys
import os
import urllib
from flask import Flask, abort, send_file, render_template, request

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
    print(os.path.dirname(__file__))
    module_path = os.path.dirname(os.path.abspath(__file__))
    scene_folder = os.path.join(module_path, 'Saves/scene')
else:
    app = Flask(__name__)
    scene_folder = 'E:/VAM/Saves/scene'

print('VAM Scene folder found at: {}'.format(scene_folder))

@app.route('/')
def index():
    sort = request.args.get('sort', None)
    term = request.args.get('filter', None)
    scenes = []

    for subdir, dirs, files in os.walk(scene_folder):
        for file in files:
            file_name, extension = os.path.splitext(file)
            url = text_encoded = urllib.parse.quote("/scenes/{}/{}".format(subdir[19:].replace('\\', '/'), file_name))

            if extension.lower() == '.vac' or extension.lower() == '.json':
                scenes.append({
                    "name": file,
                    "modified": get_modification_iso_date(subdir, file),
                    "path": url + extension,
                    "thumbnail":  url + '.jpg'
                })

    if term and len(term) > 0:
        scenes = list(filter(lambda i: term in i['name'].lower(), scenes))

    if sort == 'old':
        scenes = sorted(scenes, key = lambda i: i['modified'])
    elif sort == 'new':
        scenes = sorted(scenes, key = lambda i: i['modified'], reverse=True)
    else:
        scenes = sorted(scenes, key = lambda i: i['name'])

    return render_template('index.html', scenes=scenes, sort=sort, filter=term)

@app.route('/scenes/<path:subpath>')
def file_serve(subpath):
    absolute_path = scene_folder + '/' + subpath

    if os.path.exists(absolute_path):
        return send_file(absolute_path, as_attachment=True)
    else:
        abort(404)

def get_modification_iso_date(subdir, file):
    absolute_path = subdir + '/' + file
    return os.path.getctime(absolute_path)


if __name__ == "__main__":
    app.run(port=6969)

#import bigjson
import errno
import json
import mmap
import os
import shutil
import sys
import urllib

from flask import (
    Flask, abort, send_file, redirect, render_template, request, url_for
)

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)

module_path = os.path.abspath(__file__)
vam_path = os.path.dirname(module_path)

# Assume this module is running in a subfolder of VaM and find the installation
# root by walking up the parent folders.
while not os.path.exists(os.path.join(vam_path, 'VaM.exe')) and vam_path > '/':
    vam_path = os.path.dirname(vam_path)

# Limit browsing to Downloads folder for now.
saves_path = os.path.join(vam_path, 'Saves/Downloads')
if not os.path.exists(saves_path):
    raise FileNotFoundError(
        errno.ENOENT, os.strerror(errno.ENOENT), saves_path)

bookmarks = os.path.join(vam_path, 'browse_sites.json')
vr_startup_script = os.path.join(vam_path, 'VaM (OpenVR).bat')
desktop_startup_script = os.path.join(vam_path, 'VaM (Desktop Mode).bat')


# Flask Routes
@app.route('/')
def index():
    sort = request.args.get('sort', None)
    term = request.args.get('filter', None)
    print('Render Gallery for: {}'.format(saves_path))

    vacs = []
    with os.scandir(saves_path) as it:
        for entry in it:
            name = entry.name.lower()
            if entry.is_file() and name.endswith('.vac') and name != 'scenic.vac':
                if term:
                    if term in name:
                        vacs.append(entry)
                else:
                    vacs.append(entry)

            print(entry.stat().st_mtime)

    if sort == 'old':
        vacs = sorted(vacs, key=lambda i: i.stat().st_mtime)
    elif sort == 'new':
        vacs = sorted(vacs, key=lambda i: i.stat().st_mtime, reverse=True)
    else:
        vacs = sorted(vacs, key=lambda i: i.name)

    return render_template('index.html', vacs=vacs, sort=sort, filter=term)


@app.route('/thumbnails/<path:scene>')
def thumbnail(scene):
    print('sending >>>{}<<<'.format(scene))
    absolute_path = os.path.join(saves_path, urllib.parse.unquote(scene))
    thumbnail = absolute_path.replace('.vac', '.jpg')
    if os.path.exists(thumbnail):
        print('sending >>>{}<<<'.format(thumbnail))
        return send_file(thumbnail, as_attachment=True)
    else:
        print('>>>{}<<< not found'.format(thumbnail))
        abort(404)


@app.route('/preview/<path:scene>')
def preview(scene):
    # Preview scene from .vac by letting VAM:
    #    - "download" the vac into a copy called scenic.vac
    #    - extract it into folder at /Saves/Downloads/scenic
    #    - load the copied scene

    # delete any existing preview first
    shutil.rmtree(os.path.join(saves_path, 'scenic'), ignore_errors=True)
    absolute_path = os.path.join(saves_path, urllib.parse.unquote(scene))
    if os.path.exists(absolute_path):
        print('sending >>>{}<<<'.format(absolute_path))
        return send_file(
            absolute_path,
            as_attachment=True,
            attachment_filename='scenic.vac'
        )
    else:
        print('>>>{}<<< not found'.format(absolute_path))
        abort(404)


@app.route('/install/<path:scene>')
def install(scene):
    # TODO:
    #      - delete scenic folder
    #      - extract .vac into /Saves/Downloads/scenic
    #      -

    return "Not yet implemented."


@app.route('/settings', methods=['POST', 'GET'])
def settings():
    if request.method == 'GET':
        return render_template(
            'settings.html',
            autovr=file_contains(vr_startup_script, 'scenery.'),
            autodesk=file_contains(desktop_startup_script, 'scenery.')
        )

    if request.method == 'POST':
        print(request.form)
        # see what the user selected
        start_in_vr = 'autovr' in request.form
        start_on_desktop = 'autodesk' in request.form

        # insert auto start commands based on user's selection
        set_autostart(vr_startup_script, start_in_vr)
        set_autostart(desktop_startup_script, start_on_desktop)

        # if we are autostarting in either mode, also add a bookmark to the
        # sites list in VaM
        set_bookmark('Downloads' if start_in_vr or start_on_desktop else None)

        # go bakc to main page
        return redirect('/')


def file_contains(path, string):
    with open(path) as f:
        data = f.read()
        print(string)
        print(data)
        print(string in data)
        return string in data

    # Use these for reading scene JSON files:
    #
    # with open(bookmarks, 'rb', 0) as file, \
    #  mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
    # if s.find(b'blabla') != -1:
    #     print('true')

    # # with open(bookmarks, 'rb') as f:
    #     j = bigjson.load(f)
    #     sites = j['sites']
    #     for site in sites.to_python():
    #         if 'localhost:6969' in ','.join(site):
    #             get_bookmark = True


def set_bookmark(bookmark):
    with open(bookmarks, 'rb') as f:
        config = json.load(f)
        print(config)

        # always filter out any bookmarks pointing to VAM Scenery gallery
        # server this avoids duplicates when th euser picks a different
        # bookmark name and also dleetes the bookmark, if the user chooses to
        # disable this mod
        sites = dict(list(filter(
            lambda i: 'localhost:6969' not in i[1], config['sites']
        )))

        if bookmark:
            # add bookmark if not None
            sites[bookmark] = 'http://localhost:6969/'

        print(sites)
        # serialize back into list of lists (JSON doesn't have tuples)
        config['sites'] = [(k, v) for k, v in sites.items()]
        print(config)
        print(json.dumps(config))

    with open(bookmarks, 'w') as f:
        json.dump(config, f, indent=4)


def set_autostart(config_file, autostart):
    with open(config_file, 'r') as f:
        lines = f.readlines()

    if autostart:
        # only write start command, if it isn't in the script yet
        if 'scenery.' not in '\n'.join(lines):
            with open(config_file, 'a') as f:
                f.write('START "VaM Scenery" {}\n'.format(module_path.replace('.py', '.exe')))
    else:
        # remove start command from script
        with open(config_file, 'w') as f:
            for line in lines:
                if 'scenery.' not in line:
                    f.write(line)


if __name__ == "__main__":
    app.run(port=6969)

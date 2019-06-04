import os
import sys
import glob
import shutil
import importlib


def patch_osx_app():
    """Patch .app to copy missing data and link some libs.
    See https://github.com/pyinstaller/pyinstaller/issues/2276
    """

    app_path = sys.argv[1]

    import PyQt5

    qtwe_core_dir = PyQt5.__path__[0] + '/Qt/lib/QtWebEngineCore.framework'

    # Copy QtWebEngineProcess.app
    proc_app = 'QtWebEngineProcess.app'
    if not os.path.exists(os.path.join(app_path, 'Contents', 'MacOS', proc_app)):
        shutil.copytree(os.path.join(qtwe_core_dir, 'Helpers', proc_app),
                        os.path.join(app_path, 'Contents', 'MacOS', proc_app))

    # Copy resources
    for f in glob.glob(os.path.join(qtwe_core_dir, 'Resources', '*')):
        dest = os.path.join(app_path, 'Contents', 'Resources')
        dest = os.path.join(dest, os.path.basename(f))
        if os.path.isdir(f):
            if not os.path.exists(dest):
                shutil.copytree(f, dest)
        else:
            if not os.path.exists(dest):
                shutil.copy(f, dest)

    # Link dependencies
    for lib in ['QtCore', 'QtWebEngineCore', 'QtQuick', 'QtQml', 'QtNetwork',
                'QtGui', 'QtWebChannel', 'QtPositioning']:
        dest = os.path.join(app_path, lib + '.framework', 'Versions', '5')
        os.makedirs(dest, exist_ok=True)
        if not os.path.join(os.path.join(dest, lib)):
            os.symlink(os.path.join(os.pardir, os.pardir, os.pardir, 'Contents',
                                    'MacOS', lib),
                       os.path.join(dest, lib))

    # Copy over static files for nbformat and voila
    packages = ('voila', 'nbformat', 'nbconvert')
    for package in packages:
        path = importlib.import_module(package).__path__[0]
        if not os.path.exists(os.path.join(app_path, 'Contents', 'MacOS', package)):
            shutil.copytree(path, os.path.join(app_path, 'Contents', 'MacOS', package))

    import voila
    from voila import paths
    templates_dir = os.path.join(app_path, 'Contents', 'MacOS', 'share', 'jupyter', 'voila', 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    for path in paths.jupyter_path():
        for template in glob.glob(os.path.join(path, 'voila', 'templates', '*')):
            template_name = os.path.basename(template)
            destination = os.path.join(templates_dir, template_name)
            if not os.path.exists(destination):
                shutil.copytree(template, destination)

patch_osx_app()

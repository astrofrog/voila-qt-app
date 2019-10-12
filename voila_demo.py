import sys

# Voila (or one of its dependencies) tries to launch the kernel by calling
# python with -m ipykernel_kauncher - however it does this seemingly by using
# sys.executable, which in the case of an app is actually this script. So we
# need to catch this case and start the kernel manually.

if 'ipykernel_launcher' in sys.argv:

    if sys.path[0] == '':
        del sys.path[0]

    from ipykernel import kernelapp as app
    app.launch_new_instance()

    sys.exit(0)

if 'voila' in sys.argv:

    from voila.app import main
    main(sys.argv[3:])

    sys.exit(0)

# We put all other imports below to minimize how many imports have to be
# done in the above case where the kernel is being launched.

from subprocess import Popen

import os
import time
import socket
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

from voila.app import main

try:
    # PyQt support
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5 import QtCore
except:
    # PySide support
    from PySide2.QtWidgets import QApplication
    from PySide2.QtWebEngineWidgets import QWebEngineView
    from PySide2 import QtCore

# The following module is a fake module that contains the notebook
# to execute for now. We do this to make it easy to figure out the
# path to the file once we are in the application context
import app_notebooks  # noqa

# Find the path to the notebook
notebook = os.path.join(app_notebooks.__path__[0], 'bqplot_vuetify_example.ipynb')

# Find a free port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 0))
port = sock.getsockname()[1]
sock.close()

# Since voila needs to run its own event loop, we start it in its own process.
voila_process = Popen([sys.executable, '-m', 'voila', notebook, '--template', 'vuetify-default', '--enable_nbextensions=True', '--no-browser', '--port={0}'.format(port)])

# Wait until the server seems to respond
while True:

    print('Waiting for voila to start up...')
    time.sleep(1)

    try:
        result = urlopen('http://localhost:{0}/favicon.ico'.format(port))
        break
    except HTTPError:
        break
    except URLError:
        pass

# We need to make sure we run webengine with --single-process
# otherwise the page remains blank.
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--single-process'

app = QApplication([''])
web = QWebEngineView()
web.setUrl(QtCore.QUrl('http://localhost:{0}'.format(port)))
web.show()

# The following option is used in CI so that we can run through
# the program once without having to hang.
if '--nonblocking' in sys.argv:
    print("Running for 20s before exiting")
    start = time.time()
    while time.time() - start < 20:
        app.processEvents()
else:
    app.exec_()

voila_process.kill()
voila_process.wait()

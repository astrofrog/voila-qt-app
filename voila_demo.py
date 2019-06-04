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

# We put all other imports below to minimize how many imports have to be
# done in the above case where the kernel is being launched.

from multiprocessing import Process

import os
import time
import socket

from voila.app import main

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore

# The following module is a fake module that contains the notebook
# to execute for now. We do this to make it easy to figure out the
# path to the file once we are in the application context
import app_notebooks  # noqa

# Find the path to the notebook
notebook = os.path.join(app_notebooks.__path__[0], 'basics.ipynb')

# Find a free port
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 0))
port = sock.getsockname()[1]
sock.close()


def process_main():
    main([notebook, '--no-browser', '--port={0}'.format(port)])


# Since voila needs to run its own event loop, we start it in its own process.
voila_process = Process(target=process_main)
voila_process.start()

# Wait a little just to make sure voila has started up
time.sleep(1)

# We need to make sure we run webengine with --single-process
# otherwise the page remains blank.
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--single-process'

app = QApplication([''])
web = QWebEngineView()
web.setUrl(QtCore.QUrl('http://localhost:{0}'.format(port)))
web.show()

# The following option is used in CI so that we can run through
# the program once without having to hang.
if '--nonblocking' not in sys.argv:
    app.exec_()

import sys

if 'ipykernel_launcher' in sys.argv:

    if sys.path[0] == '':
        del sys.path[0]

    from ipykernel import kernelapp as app
    app.launch_new_instance()

    sys.exit(0)

import multiprocessing
multiprocessing.freeze_support()

from multiprocessing import Process

from voila.app import main

import os
import time
import tempfile
import app_notebooks  # noqa

import pkgutil

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore

# notebook_content = pkgutil.get_data('app_notebooks', 'basics.ipynb')
# tmpdir = tempfile.mkdtemp()
notebook = os.path.join(app_notebooks.__path__[0], 'basics.ipynb')

os.environ['JOBLIB_MULTIPROCESSING'] = '0'

def process_main():
    os.environ['JOBLIB_MULTIPROCESSING'] = '0'
    main([notebook, '--no-browser', '--port=8789'])

# Note: can't use voila in a thread, so need to use a process
voila_process = Process(target=process_main)
voila_process.start()

time.sleep(2)

os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--single-process'

app = QApplication([''])
web = QWebEngineView()
web.setUrl(QtCore.QUrl('http://localhost:8789'))
web.show()

if '--nonblocking' not in sys.argv:
    app.exec_()

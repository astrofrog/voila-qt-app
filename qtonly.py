import os
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5 import QtCore

os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--single-process'

app = QApplication([''])
web = QWebEngineView()
web.setUrl(QtCore.QUrl('http://worldwidetelescope.org/webclient/'))
web.show()

if '--nonblocking' not in sys.argv:
    app.exec_()

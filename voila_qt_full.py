from multiprocessing import Process

from voila.app import main

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5 import QtCore

# Note: can't use voila in a thread, so need to use a process
voila_process = Process(target=main, args=[['basics.ipynb', '--no-browser']])
voila_process.start()

app = QApplication([''])
web = QWebEngineView()
page = QWebEnginePage()
page.setView(web)
web.setPage(page)
web.setUrl(QtCore.QUrl('http://localhost:8866/'))
web.show()
app.exec_()

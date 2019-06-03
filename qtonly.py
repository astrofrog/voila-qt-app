from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5 import QtCore

app = QApplication([''])
web = QWebEngineView()
page = QWebEnginePage()
page.setView(web)
web.setPage(page)
web.setUrl(QtCore.QUrl('http://www.google.com/'))
web.show()
app.processEvents()

# don't execute the app so we can try running it in CI without blocking

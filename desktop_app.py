import sys
import threading
import time
import os
import uvicorn
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile
from PyQt6.QtCore import QUrl

if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

backend_path = os.path.join(application_path, "backend")
sys.path.append(backend_path)
os.chdir(backend_path)

from main import app

def start_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="critical")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Görüntü İşleme Projesi - Masaüstü")
        self.setGeometry(100, 100, 1200, 800)
        
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://127.0.0.1:8000"))
        
        QWebEngineProfile.defaultProfile().downloadRequested.connect(self.handle_download)
        
        self.setCentralWidget(self.browser)
    
    def handle_download(self, download):
        suggested_name = download.downloadFileName() or "islenmis_goruntu.png"
        path, _ = QFileDialog.getSaveFileName(self, "Görüntüyü Kaydet", suggested_name, "PNG Dosyası (*.png);;Tüm Dosyalar (*)")
        if path:
            download.setDownloadFileName(os.path.basename(path))
            download.setDownloadDirectory(os.path.dirname(path))
            download.accept()
        else:
            download.cancel()

if __name__ == '__main__':
    server_thread = threading.Thread(target=start_fastapi)
    server_thread.daemon = True
    server_thread.start()
    
    time.sleep(1.5)
    
    qt_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(qt_app.exec())

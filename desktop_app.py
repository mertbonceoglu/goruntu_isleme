import sys
import threading
import time
import os
import uvicorn
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

# Frontend ve Backend yollarını ayarlama (PyInstaller uyumluluğu)
if getattr(sys, 'frozen', False):
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

# backend klasörünü path'e ekliyoruz ki main.py içindeki modüller bulunabilsin
backend_path = os.path.join(application_path, "backend")
sys.path.append(backend_path)
os.chdir(backend_path) # Statik dosyaların bulunabilmesi için çalışma dizinini değiştir

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
        
        self.setCentralWidget(self.browser)

if __name__ == '__main__':
    # FastAPI Sunucusunu arka planda başlat
    server_thread = threading.Thread(target=start_fastapi)
    server_thread.daemon = True
    server_thread.start()
    
    # Sunucunun ayağa kalkması için kısa bir süre bekle
    time.sleep(1.5)
    
    # PyQt ile masaüstü penceresini başlat
    qt_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(qt_app.exec())

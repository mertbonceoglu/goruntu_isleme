@echo off
echo Masaustu uygulamasi derleniyor... lutfen bekleyin.
backend\venv\Scripts\pyinstaller --noconfirm --onedir --windowed --add-data "frontend;frontend" desktop_app.py
echo Derleme tamamlandi! Program 'dist\desktop_app' klasoru icerisindedir.
pause

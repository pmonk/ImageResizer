@echo off
echo Installing requirements...
pip install pillow tkinterdnd2 pyinstaller

echo Downloading PyInstaller hook...
curl -o hook-tkinterdnd2.py https://raw.githubusercontent.com/pmgagne/tkinterdnd2/master/hook-tkinterdnd2.py

echo Building ImageResizer.exe...
REM Use python -m PyInstaller (bypasses PATH issue)
python -m PyInstaller --onefile --windowed --name "ImageResizer" --icon=image.ico image_resizer.py --additional-hooks-dir=.

echo SUCCESS! EXE in /dist/ImageResizer.exe
echo Test: Double-click dist/ImageResizer.exe
echo Cleanup: rmdir /s /q build dist  ^& del *.spec hook-tkinterdnd2.py
pause

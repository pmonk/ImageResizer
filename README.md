# ImageResizer - Batch Web Image Optimizer GUI

![Demo](screenshot.png)

Drag & drop folder, pick size (1920/1200/800px), get optimized JPGs in /resized/.

## Features
- Drag-drop folders
- Web presets: 1920px hero, 1200px large, 800px thumbs
- Smart skip small images (optional copy)
- Recursive subfolder scan
- Progress + stats
- Standalone Windows EXE

## Quick Start - Windows EXE
1. Download ImageResizer.exe (Releases tab)
2. Double-click icon
3. Drag folder or Browse
4. Pick size, Resize Images
5. Output: /resized/ folder

## Python
pip install pillow tkinterdnd2
python image_resizer.py

## Build EXE
Download image.ico + run build_exe.bat

## Example
Input photos/
- IMG_001.jpg (4000x3000, 7MB)

Output photos/resized/
- IMG_001.jpg (1920px max, 180KB)

## Sample Results
Original     | Resized     | Savings
-------------|-------------|--------
4000x3000 7MB| 1920x1440 185KB | 97%
3000x4000 5MB| 1200x1600 112KB | 98%

## Tech
Python 3.8+ / Tkinter (built-in GUI), Pillow, tkinterdnd2, PyInstaller

## Credits
- Icon: FadeMind/W-ICO (Public Domain)
- tkinterdnd2: pmgagne
- Perplexity AI: Script help
- Pillow: Image optimization

## License
MIT © 2026 pmonk.com

Free for personal, commercial, whatever. No warranty. Test on copies first!

# DeskBrush

A transparent desktop overlay drawing and annotation tool built with PyQt5.

![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-blue) ![PyQt5](https://img.shields.io/badge/PyQt5-5.15-green) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Features

- **Full-screen transparent canvas** — Draw on top of any desktop application
- **Pen tool** — Freehand drawing with smooth Bezier curves
- **Text tool** — Click to place text with customizable font size
- **8 colors** — Red, Blue, Green, Black, White, Yellow, Orange, Purple
- **3 sizes** — Small, Medium, Large (controls stroke width or font size)
- **Draw/Pass mode** — Toggle canvas visibility to interact with desktop apps
- **Undo / Clear** — One-click stroke or text removal
- **Frosted-glass toolbar** — Draggable, semi-transparent, rounded corners

## Quick Start (No Installation Required)

**For Windows users:**

1. Go to [Releases](https://github.com/leelydia1101/DeskBrush/releases/latest)
2. Download `DeskBrush.exe`
3. Double-click to run — no Python or dependencies needed!

## Development

### Prerequisites

```bash
pip install PyQt5
```

### Run from Source

```bash
python main.py
```

### Build Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico --name DeskBrush main.py
```

The executable will be in `dist/DeskBrush.exe`.

## Controls

| Action | Shortcut |
|--------|----------|
| Toggle Draw/Pass mode | `Ctrl+D` |
| Undo | `Ctrl+Shift+Z` |
| Clear all | `Ctrl+Shift+C` |
| Quit | `Esc` |

## Project Structure

```
deskbrush/
├── main.py           # Application entry point
├── canvas.py         # Transparent overlay canvas (pen + text)
├── toolbar.py        # Frosted-glass floating toolbar
├── icon.ico          # Application icon
└── requirements.txt  # Dependencies
```

## License

MIT

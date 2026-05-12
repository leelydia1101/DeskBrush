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

## Installation

```bash
pip install PyQt5
```

## Usage

```bash
python main.py
```

### Controls

| Action | Shortcut / Button |
|--------|-------------------|
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
└── requirements.txt  # Dependencies
```

## License

MIT

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QColor
from PyQt5.QtWidgets import QApplication
from canvas import Canvas
from toolbar import Toolbar


class DeskBrush:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.canvas = Canvas()
        self.toolbar = Toolbar()

        self.toolbar.move(20, 20)
        self.toolbar.show()

        self.canvas.set_toolbar_rect(self.toolbar.geometry())
        self.toolbar.moved.connect(lambda: self.canvas.set_toolbar_rect(self.toolbar.geometry()))
        self.toolbar.resized.connect(lambda: self.canvas.set_toolbar_rect(self.toolbar.geometry()))
        self.toolbar.mode_changed.connect(self.canvas.set_drawing_mode)
        self.toolbar.tool_changed.connect(self.canvas.set_tool)
        self.toolbar.color_changed.connect(self._on_color_changed)
        self.toolbar.width_changed.connect(self._on_width_changed)
        self.toolbar.undo_clicked.connect(self.canvas.undo)
        self.toolbar.clear_clicked.connect(self.canvas.clear)
        self.toolbar.close_clicked.connect(self.app.quit)

        self._setup_shortcuts()

    def _setup_shortcuts(self):
        from PyQt5.QtWidgets import QShortcut
        shortcut_d = QShortcut(QKeySequence("Ctrl+D"), self.toolbar)
        shortcut_d.activated.connect(self._toggle_mode)
        shortcut_d.setContext(Qt.ApplicationShortcut)
        shortcut_z = QShortcut(QKeySequence("Ctrl+Shift+Z"), self.toolbar)
        shortcut_z.activated.connect(self.canvas.undo)
        shortcut_z.setContext(Qt.ApplicationShortcut)
        shortcut_c = QShortcut(QKeySequence("Ctrl+Shift+C"), self.toolbar)
        shortcut_c.activated.connect(self.canvas.clear)
        shortcut_c.setContext(Qt.ApplicationShortcut)
        shortcut_esc = QShortcut(QKeySequence("Esc"), self.toolbar)
        shortcut_esc.activated.connect(self.app.quit)
        shortcut_esc.setContext(Qt.ApplicationShortcut)

    def _toggle_mode(self):
        self._is_draw_mode = not getattr(self, "_is_draw_mode", True)
        self.canvas.set_drawing_mode(self._is_draw_mode)
        self.toolbar.mode_btn.setText("Draw" if self._is_draw_mode else "Pass")
        self.toolbar.mode_btn.setChecked(self._is_draw_mode)

    def _on_color_changed(self, color: QColor):
        self.canvas.current_color = color

    def _on_width_changed(self, width: int):
        self.canvas.current_width = width

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = DeskBrush()
    app.run()

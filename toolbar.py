from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen, QFont
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QButtonGroup, QLabel, QFrame
)


class Toolbar(QWidget):
    mode_changed = pyqtSignal(bool)
    tool_changed = pyqtSignal(str)
    color_changed = pyqtSignal(QColor)
    width_changed = pyqtSignal(int)
    undo_clicked = pyqtSignal()
    clear_clicked = pyqtSignal()
    close_clicked = pyqtSignal()
    moved = pyqtSignal()
    resized = pyqtSignal()

    COLORS = [
        ("red", QColor(255, 0, 0)),
        ("blue", QColor(0, 120, 255)),
        ("green", QColor(0, 180, 0)),
        ("black", QColor(0, 0, 0)),
        ("white", QColor(255, 255, 255)),
        ("yellow", QColor(255, 220, 0)),
        ("orange", QColor(255, 140, 0)),
        ("purple", QColor(160, 0, 240)),
    ]

    SIZES = [
        ("S", 2),
        ("M", 5),
        ("L", 10),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedHeight(100)
        self._drag_pos = None
        self._is_drawing_mode = True
        self._current_tool = "pen"
        self._init_ui()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        rect = QRectF(self.rect())
        path.addRoundedRect(rect, 20, 20)
        painter.fillPath(path, QColor(45, 45, 45, 150))
        painter.end()

    def _init_ui(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(60, 60, 60, 120);
                color: #f5f5f5;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-family: 'Segoe UI', sans-serif;
            }
            QPushButton:hover {
                background-color: rgba(80, 80, 80, 150);
            }
            QPushButton:checked {
                background-color: rgba(100, 100, 100, 180);
                border: 2px solid rgba(255, 255, 255, 100);
            }
            QLabel {
                color: #e0e0e0;
                font-size: 13px;
                font-family: 'Segoe UI', sans-serif;
                background: transparent;
            }
        """)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 12, 15, 12)
        main_layout.setSpacing(10)

        # Mode button (Draw/Pass)
        self.mode_btn = QPushButton("Draw")
        self.mode_btn.setCheckable(True)
        self.mode_btn.setChecked(True)
        self.mode_btn.setFixedSize(90, 70)
        self.mode_btn.clicked.connect(self._on_mode_clicked)
        main_layout.addWidget(self.mode_btn)

        main_layout.addWidget(self._separator())

        # Tool selection (Pen/Text)
        tool_layout = QVBoxLayout()
        tool_layout.setSpacing(4)
        tool_layout.addWidget(QLabel("Tool"), alignment=Qt.AlignCenter)
        tool_row = QHBoxLayout()
        tool_row.setSpacing(4)
        self.tool_group = QButtonGroup(self)
        self.pen_btn = QPushButton("✏")
        self.pen_btn.setCheckable(True)
        self.pen_btn.setChecked(True)
        self.pen_btn.setFixedSize(60, 50)
        self.pen_btn.clicked.connect(lambda: self._on_tool_clicked("pen"))
        self.tool_group.addButton(self.pen_btn)
        tool_row.addWidget(self.pen_btn)
        self.text_btn = QPushButton("T")
        self.text_btn.setCheckable(True)
        self.text_btn.setFixedSize(60, 50)
        self.text_btn.clicked.connect(lambda: self._on_tool_clicked("text"))
        self.tool_group.addButton(self.text_btn)
        tool_row.addWidget(self.text_btn)
        tool_layout.addLayout(tool_row)
        main_layout.addLayout(tool_layout)

        main_layout.addWidget(self._separator())

        # Color selection
        color_layout = QVBoxLayout()
        color_layout.setSpacing(4)
        color_layout.addWidget(QLabel("Color"), alignment=Qt.AlignCenter)
        color_row = QHBoxLayout()
        color_row.setSpacing(4)
        self.color_group = QButtonGroup(self)
        self.color_btns = []
        for i, (name, color) in enumerate(self.COLORS):
            btn = QPushButton()
            btn.setFixedSize(36, 36)
            btn.setCheckable(True)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba({color.red()}, {color.green()}, {color.blue()}, 255);
                    border: none;
                    border-radius: 18px;
                }}
                QPushButton:hover {{
                    border: 2px solid rgba(255, 255, 255, 120);
                }}
                QPushButton:checked {{
                    border: 2px solid rgba(255, 255, 255, 180);
                }}
            """)
            btn.clicked.connect(lambda checked, c=color: self._on_color_clicked(c))
            self.color_group.addButton(btn, i)
            self.color_btns.append(btn)
            color_row.addWidget(btn)
        self.color_btns[0].setChecked(True)
        color_layout.addLayout(color_row)
        main_layout.addLayout(color_layout)

        main_layout.addWidget(self._separator())

        # Size selection
        size_layout = QVBoxLayout()
        size_layout.setSpacing(4)
        size_layout.addWidget(QLabel("Size"), alignment=Qt.AlignCenter)
        size_row = QHBoxLayout()
        size_row.setSpacing(4)
        self.size_group = QButtonGroup(self)
        self.size_btns = []
        for i, (label, size) in enumerate(self.SIZES):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setFixedSize(50, 50)
            btn.clicked.connect(lambda checked, s=size: self._on_size_clicked(s))
            self.size_group.addButton(btn, i)
            self.size_btns.append(btn)
            size_row.addWidget(btn)
        self.size_btns[1].setChecked(True)
        size_layout.addLayout(size_row)
        main_layout.addLayout(size_layout)

        main_layout.addWidget(self._separator())

        # Action buttons (icons only)
        action_layout = QVBoxLayout()
        action_layout.setSpacing(4)
        action_row = QHBoxLayout()
        action_row.setSpacing(6)
        self.undo_btn = QPushButton("⟲")
        self.undo_btn.setToolTip("Undo")
        self.undo_btn.setFixedSize(50, 50)
        self.undo_btn.clicked.connect(self.undo_clicked.emit)
        action_row.addWidget(self.undo_btn)
        self.clear_btn = QPushButton("🗑")
        self.clear_btn.setToolTip("Clear")
        self.clear_btn.setFixedSize(50, 50)
        self.clear_btn.clicked.connect(self.clear_clicked.emit)
        action_row.addWidget(self.clear_btn)
        self.close_btn = QPushButton("✕")
        self.close_btn.setToolTip("Close")
        self.close_btn.setFixedSize(50, 50)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(180, 60, 60, 150);
                color: #f5f5f5;
                border: none;
                border-radius: 10px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: rgba(200, 80, 80, 180);
            }
        """)
        self.close_btn.clicked.connect(self.close_clicked.emit)
        action_row.addWidget(self.close_btn)
        action_layout.addLayout(action_row)
        main_layout.addLayout(action_layout)

        self.setLayout(main_layout)

    def _separator(self) -> QFrame:
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setStyleSheet("background: transparent; border: 1px solid rgba(150, 150, 150, 60);")
        sep.setFixedWidth(2)
        return sep

    def _on_mode_clicked(self):
        self._is_drawing_mode = not self._is_drawing_mode
        self.mode_btn.setText("Draw" if self._is_drawing_mode else "Pass")
        self.mode_changed.emit(self._is_drawing_mode)

    def _on_tool_clicked(self, tool: str):
        self._current_tool = tool
        self.tool_changed.emit(tool)

    def _on_color_clicked(self, color: QColor):
        for btn in self.color_btns:
            btn.setChecked(False)
        sender = self.sender()
        if sender in self.color_btns:
            sender.setChecked(True)
        self.color_changed.emit(color)

    def _on_size_clicked(self, size: int):
        for btn in self.size_btns:
            btn.setChecked(False)
        sender = self.sender()
        if sender in self.size_btns:
            sender.setChecked(True)
        self.width_changed.emit(size)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None:
            self.move(event.globalPos() - self._drag_pos)
            self.moved.emit()
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
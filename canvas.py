from dataclasses import dataclass, field
from typing import List, Optional

from PyQt5.QtCore import QPointF, Qt, QRect
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QPen, QRegion, QFont
from PyQt5.QtWidgets import QWidget, QLineEdit


@dataclass
class Stroke:
    points: List[QPointF] = field(default_factory=list)
    color: QColor = field(default_factory=lambda: QColor(255, 0, 0))
    width: int = 5


@dataclass
class TextItem:
    pos: QPointF = field(default_factory=lambda: QPointF(0, 0))
    text: str = ""
    color: QColor = field(default_factory=lambda: QColor(255, 0, 0))
    font_size: int = 20


class Canvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.setCursor(Qt.CrossCursor)

        self.strokes: List[Stroke] = []
        self.texts: List[TextItem] = []
        self.current_stroke: Stroke = None
        self.is_drawing = False
        self.drawing_enabled = True
        self.current_color = QColor(255, 0, 0)
        self.current_width = 5
        self.current_tool = "pen"
        self.toolbar_rect: Optional[QRect] = None
        self._active_line_edit = None

        self.showFullScreen()

    def set_toolbar_rect(self, rect: QRect):
        self.toolbar_rect = rect
        self._update_mask()

    def _update_mask(self):
        if self.toolbar_rect is None:
            self.clearMask()
            return
        full_region = QRegion(self.rect())
        toolbar_region = QRegion(self.toolbar_rect)
        masked_region = full_region.subtracted(toolbar_region)
        self.setMask(masked_region)

    def set_drawing_mode(self, enabled: bool):
        self.drawing_enabled = enabled
        self.setVisible(enabled)
        if enabled:
            self._update_mask()
            self.setCursor(Qt.CrossCursor)

    def set_tool(self, tool: str):
        self._finish_text_input()
        self.current_tool = tool
        if tool == "text":
            self.setCursor(Qt.IBeamCursor)
        else:
            self.setCursor(Qt.CrossCursor)

    def _finish_text_input(self):
        if self._active_line_edit is not None:
            text = self._active_line_edit.text().strip()
            if text:
                font_sizes = {2: 14, 5: 20, 10: 28}
                self.texts.append(TextItem(
                    pos=self._active_line_edit._origin_pos,
                    text=text,
                    color=QColor(self.current_color),
                    font_size=font_sizes.get(self.current_width, 20),
                ))
            self._active_line_edit.deleteLater()
            self._active_line_edit = None
            self.update()

    def undo(self):
        self._finish_text_input()
        if self.texts:
            self.texts.pop()
            self.update()
        elif self.strokes:
            self.strokes.pop()
            self.update()

    def clear(self):
        self._finish_text_input()
        self.strokes.clear()
        self.texts.clear()
        self.current_stroke = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 1))
        for stroke in self.strokes:
            self._draw_stroke(painter, stroke)
        if self.current_stroke and self.current_stroke.points:
            self._draw_stroke(painter, self.current_stroke)
        for text_item in self.texts:
            self._draw_text(painter, text_item)
        painter.end()

    def _draw_stroke(self, painter: QPainter, stroke: Stroke):
        if len(stroke.points) < 2:
            if len(stroke.points) == 1:
                painter.setPen(Qt.NoPen)
                painter.setBrush(stroke.color)
                r = stroke.width / 2
                painter.drawEllipse(stroke.points[0], r, r)
            return
        painter.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(stroke.points[0])
        for i in range(1, len(stroke.points) - 1):
            mid = (stroke.points[i] + stroke.points[i + 1]) / 2
            path.quadTo(stroke.points[i], mid)
        path.lineTo(stroke.points[-1])
        pen = QPen(stroke.color, stroke.width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.drawPath(path)

    def _draw_text(self, painter: QPainter, item: TextItem):
        font = QFont("Microsoft YaHei", item.font_size)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(item.color)
        painter.drawText(item.pos, item.text)

    def mousePressEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        if self.current_tool == "text":
            self._finish_text_input()
            line_edit = QLineEdit(self)
            line_edit._origin_pos = QPointF(event.pos())
            line_edit.move(event.pos())
            line_edit.setFixedSize(500, 60)
            line_edit.setStyleSheet("""
                QLineEdit {
                    background-color: rgba(0, 0, 0, 200);
                    color: white;
                    border: 2px solid #888;
                    border-radius: 6px;
                    padding: 10px 14px;
                    font-size: 22px;
                }
            """)
            line_edit.returnPressed.connect(self._finish_text_input)
            line_edit.show()
            line_edit.setFocus()
            self._active_line_edit = line_edit
            return
        self.is_drawing = True
        self.current_stroke = Stroke(
            points=[QPointF(event.pos())],
            color=QColor(self.current_color),
            width=self.current_width,
        )

    def mouseMoveEvent(self, event):
        if not self.is_drawing or not self.current_stroke:
            return
        self.current_stroke.points.append(QPointF(event.pos()))
        self.update()

    def mouseReleaseEvent(self, event):
        if not self.is_drawing:
            return
        self.is_drawing = False
        if self.current_stroke and self.current_stroke.points:
            self.strokes.append(self.current_stroke)
        self.current_stroke = None
        self.update()

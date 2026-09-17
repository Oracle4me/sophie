from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QApplication, QWidget


class SophieDesktop(QWidget):
    """Floating desktop shell Sophie."""

    def __init__(self) -> None:
        super().__init__()
        self.drag_position: QPoint | None = None

        self.setWindowTitle("Sophie")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )
        self.setFixedSize(320, 420)
        self.move_to_screen_corner()

    def move_to_screen_corner(self) -> None:
        screen = QApplication.primaryScreen()
        if screen is None:
            return

        geometry = screen.availableGeometry()
        margin = 32

        x = geometry.right() - self.width() - margin
        y = geometry.bottom() - self.height() - margin

        self.move(x, y)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 0))
        painter.drawRect(self.rect())

        painter.setBrush(QColor(35, 35, 45, 220))
        painter.drawRoundedRect(
            40,
            80,
            240,
            280,
            30,
            30,
        )

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        if (
            self.drag_position is not None
            and event.buttons() & Qt.MouseButton.LeftButton
        ):
            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )
            event.accept()

    def mouseReleaseEvent(self, event) -> None:
        self.drag_position = None
        event.accept()

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.RightButton:
            self.close()


def run_desktop() -> None:
    app = QApplication.instance() or QApplication([])
    window = SophieDesktop()
    window.show()
    app.exec()
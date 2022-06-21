from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class GadgetIcon(QWidget):
    def __init__(self, icon, marks = False):
        super().__init__()

        self.marks = marks
        self.icon = QPixmap(icon)
        self.track_marks = QPixmap(r'TrackingMarks.png')
        self.effect = QGraphicsColorizeEffect(self)
        self.effect.setColor(QColor("White"))
        self.setGraphicsEffect(self.effect)
        self.setFixedSize(QSize(58,58))
        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding
        )

    def sizeHint(self):
        return QSize(58,58)

    def paintEvent(self, e):
        painter = QPainter(self)
        if self.marks:
            rect = QRect(0,0,painter.device().width(), painter.device().height())
            painter.drawPixmap(rect, self.track_marks)
        rect = QRect((painter.device().width() - 48) / 2, 10, 48, 48)
        painter.drawPixmap(rect, self.icon)

    def showMarks(self, val):
        self.marks = val


class MapElement(QWidget):

    name = ""
    tags = []
    icon_file = ""
    isTracked = False
    tint_color = QColor("White")
    uuid = ""

    clicked = Signal(object)

    def __init__(self, name = "", tags = [], icon_file="mcu.png", isTracked = False, uuid=""):
        super().__init__()

        self.setSizePolicy(
            QSizePolicy.MinimumExpanding,
            QSizePolicy.MinimumExpanding
        )
        self.uuid = uuid
        self.name = name
        self.tags = tags
        self.icon_file = icon_file
        self.isTracked = isTracked

        self.icon = GadgetIcon(self.icon_file, marks=self.isTracked)
        self.lbl = QLabel(self.name)
        self.lbl.setAlignment(Qt.AlignCenter)
        self.lbl.setFont(QFont('PT Sans', 14))
        tagline = ""
        for i in self.tags:
            tagline = tagline + str(i) + ', ' 
        self.sublbl = QLabel()
        self.sublbl.setText(tagline)
        self.sublbl.setAlignment(Qt.AlignCenter)
        self.sublbl.setFont(QFont('PT Sans', 10))

        self.setFixedSize(QSize(90,120))

        l = QVBoxLayout()
        l.addWidget(self.icon)
        l.addWidget(self.lbl)
        l.addWidget(self.sublbl)
        self.setLayout(l)


    def sizeHint(self):
        return QSize(70, 100)

    def refresh(self):
        self.lbl.setText(self.name)
        tagline = ""
        for i in self.tags:
            tagline = tagline + str(i) + ', '
        self.sublbl.setText(tagline)
        self.icon.showMarks(self.isTracked)


    def mousePressEvent(self, e):
        self.clicked.emit(self.uuid)
        

# if __name__ == '__main__':
#     import sys
    
#     app = QApplication(sys.argv)

#     widget = MapElement(name="Lamp", tags=["Kitchen", "RGB"], icon_file="lamp.png", isTracked=True)
#     widget.show()

#     app.exec_()

import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from dashparser import DashParser
from netmap import NetListView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(800, 600))
        self.setWindowTitle("Управление устройствами")
        self.layout = QStackedLayout()
        # self.layout.addWidget(self.net_view)

        widget = QWidget()
        widget.setLayout(self.layout)

        self.open_net_view()

    @Slot(object)
    def open_gadget(self, uuid):
        view = DashParser(self, uuid)
        self.setCentralWidget(view)

    def open_net_view(self):
        net_view = NetListView(self)
        self.setCentralWidget(net_view)
        

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec_()
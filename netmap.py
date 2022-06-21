import os
from pathlib import Path
import json
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from icon import MapElement

class NetListView(QWidget):

    gadget_list = [] # array of dicts of gadgets with UUIDs

    def __init__(self, parent):

        super().__init__()

        self.parent = parent
        
        self.path_to_gadgets = Path("~/Gadgets")
        print(self.path_to_gadgets)
        self.path_to_icons = self.path_to_gadgets / "Configuration" / "DefaultIcons"
        self.setFixedSize(QSize(800,600))
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.refresh()

    def sizeHint(self):
        return QSize(800, 600)

    def update_gadgets(self):
        self.gadget_list.clear()
        arr = self.path_to_gadgets.expanduser().glob('*')
        dirs = [x for x in arr if x.is_dir() and x.name != 'Configuration']
        path = 'Info.json'
        print(dirs)
        for i in dirs:
            p = self.path_to_gadgets / i
            if p.is_dir():
                if (p / path).exists():
                    with (p / path).open() as f:
                        # try:
                        d = json.load(f)
                        d['uuid'] = i.name
                        print('GADGET' + str(d))
                        self.gadget_list.append(d)
                        # except:
                        #     print("Smth went wrong")

    def draw_view(self):
        col = 0
        row = 0
        for i in self.gadget_list:
            if col > 4:
                col = 0

            try:
                print(i["Icon"])
                print(i["Name"])
                print(i["uuid"])
            except:
                print("Bad dict" + str(i))
                return

            icon = self.path_to_icons / i["Icon"]
            if not icon.exists():
                icon = self.path_to_gadgets.expanduser() / i["uuid"] / i["Icon"]
                if not icon.exists():
                    icon = ""
            print('Icon: ' + str(icon))
            el = MapElement(name=i["Name"], icon_file=str(icon), uuid=i["uuid"])
            el.clicked.connect(self.parent.open_gadget)
            self.layout.addWidget(el, col, row)

            col = col + 1
            row = row + 1

    def refresh(self):
        self.update_gadgets()
        self.draw_view()
    






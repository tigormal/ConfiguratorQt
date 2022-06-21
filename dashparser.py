import yaml
from pathlib import Path
from PySide2.QtWidgets import *
from PySide2.QtCore import *


class DashParser(QWidget):

    dashboard = None
    views = []
    context = dict()
    uuid = ""

    def __init__(self, parent, uuid, filename='dashboard.yaml', name="Панель управления"):
        super().__init__()

        self.parent = parent
        self.uuid = uuid
        self.path_to_sink = Path('~/Gadgets/sink').expanduser()
        self.path_to_dashboard = Path('~/Gadgets').expanduser() / self.uuid / filename
        self.update_context()

        self.layout = QVBoxLayout()
        bar = QHBoxLayout()
        self.back = QPushButton('Назад')
        self.back.pressed.connect(self.parent.open_net_view)
        self.title = QLabel(name)
        bar.addWidget(self.back)
        bar.addWidget(self.title)
        bar.addStretch()
        w = QWidget()
        w.setLayout(bar)
        self.layout.addWidget(w)
        self.layout.addStretch()

        self.open(str(self.path_to_dashboard))

        self.setLayout(self.layout)

    def open(self, file_path):
        # with open(file_path, "r") as stream:
        #     try:
        #         self.dashboard = yaml.safe_load(stream)
        #         print(self.dashboard)
        #     except yaml.YAMLError as exc:
        #         print(exc)
        self.dashboard = yaml.safe_load(Path(file_path).read_text())
        print(self.dashboard)

        if self.dashboard is not None:
            if self.dashboard["View Main"] is not None:
                self.process_view(self.dashboard["View Main"], self.layout)
                self.layout.addStretch()
                self.update()
            else:
                print("No Main view found!")
                return
    
    def update_context(self):
        path = Path('~/Gadgets').expanduser() / self.uuid / "data"
        a = path.glob('*')
        arr = [x for x in a if x.is_file() and not x.name.startswith('.')]
        print(arr)
        for i in arr:
            with (path / i).open() as f:
                self.context[str(i.name)] = f.readline()
                print(self.context[str(i.name)])

    def send_message(self, ack=0):
        str = self.message_to_send
        msg = self.uuid + '\n' + str
        if ack :
            msg = msg + '\n' + 'ACK'
        msg = msg + '\n'
        with open(self.path_to_sink, "w") as f:
            print('have opened sink, commencing writing...')
            f.write(msg)

    def process_view(self, view, parent_layout):
        # print("process_view")
        # print(view)
        if isinstance(view, list):
            for val in view:
                w = QStackedLayout()
                self.process_view(val, w)
                q = QWidget()
                q.setLayout(w)
                parent_layout.addWidget(q)
        elif isinstance(view, dict):
            for key in view.keys():
                val = view[key]
                if key == 'Button':
                    print("found button")
                    w = QPushButton()
                    # print(val.items())
                    for k, v in val.items():
                        if k == 'Title':
                            w.setText(v)
                        elif k == 'Size':
                            s = v.split()
                            w.setFixedSize(QSize(int(s[0]), int(s[1])))
                        if k == 'AltTitle':
                            pass
                        if k == 'Action':
                            for i in v:
                                s = str(i)
                                if s.startswith('tell'):
                                    s.removeprefix('tell ')
                                    self.message_to_send = s
                                    w.pressed.connect(self.send_message)
                                elif s.startswith('log'):
                                    s.removeprefix('tell ')
                                    print('[LOG]'+ s)
                    parent_layout.addWidget(w)
                if key == 'Text':
                    print("found text")
                    w = QLabel()
                    for k, v in val.items():
                        if k == 'Value':
                            w.setText(v)
                        elif k == 'Source':
                            try:
                                s = self.context[v]
                                w.setText(s)
                            except:
                                print("Couldn't get context value" + str(self.context))
                        elif k == 'Size':
                            s = v.split()
                            w.setFixedSize(QSize(int(s[0]), int(s[1])))
                        elif k == 'AltTitle':
                            pass
                    parent_layout.addWidget(w)
                elif key == 'VStack':
                    print("found vstack")
                    w = QVBoxLayout()
                    self.process_view(val, w)
                    w.addStretch()
                    q = QWidget()
                    q.setLayout(w)
                    parent_layout.addWidget(q)
                elif key == 'HStack':
                    print("found hstack")
                    w = QHBoxLayout()
                    self.process_view(val, w)
                    w.addStretch()
                    q = QWidget()
                    q.setLayout(w)
                    parent_layout.addWidget(q)
        else:
            print('Bad view given!')



from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from copy import deepcopy


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            try:
                return self._data[index.row()][index.column()]
            except IndexError:
                return ""

        if role == Qt.ForegroundRole:
            try:
                if index.column() > 0:
                    if "stall" in self._data[index.row()][index.column()]:
                        return QColor("blue")
                    elif "flush" in self._data[index.row()][index.column()]:
                        return QColor("red")
            except IndexError:
                pass

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[-1])


class StageView(QTableView):
    def __init__(self):
        super().__init__()

        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)

        self.setSelectionMode(QAbstractItemView.NoSelection)

        # Enable drag scroll
        self.qscroller = QScroller.scroller(self)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        props = self.qscroller.scrollerProperties()
        props.setScrollMetric(QScrollerProperties.HorizontalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        props.setScrollMetric(QScrollerProperties.VerticalOvershootPolicy, QScrollerProperties.OvershootAlwaysOff)
        props.setScrollMetric(QScrollerProperties.MaximumVelocity, 0)
        props.setScrollMetric(QScrollerProperties.MinimumVelocity, 0)
        self.qscroller.setScrollerProperties(props)
        self.qscroller.grabGesture(self, QScroller.LeftMouseButtonGesture)

    def update_view(self, simulator):
        data_copy = deepcopy(simulator.pipeline.stage_information)
        data_copy.insert(0, ["Instruction"] + [str(x) for x in list(range(len(data_copy[-1]) - 1))])
        self.model = TableModel(data_copy)
        self.setModel(self.model)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # for x in range(len(data_copy)):
        #     self.horizontalHeader().setSectionResizeMode(x, QHeaderView.ResizeToContents)
        self.horizontalHeader().setDefaultSectionSize(80)
        self.scrollToBottom()
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().maximum())

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = StageView()
    window.show()
    sys.exit(app.exec_())

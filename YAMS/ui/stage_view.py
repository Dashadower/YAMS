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


class StageViewFrozen(QTableView):
    def __init__(self, parent=None, fixed_col_count=1, *args):
        QTableView.__init__(self, parent, *args)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setSelectionMode(QAbstractItemView.NoSelection)


        self._fixed_col_count = fixed_col_count
        self._fixed_row_count = 1

        self.frozenTableView = QTableView(self)

        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.setFocusPolicy(Qt.NoFocus)
        self.frozenTableView.setStyleSheet('''border: none; background-color: #CCC''')
        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.frozenTableView.verticalHeader().setVisible(False)
        self.frozenTableView.horizontalHeader().setVisible(False)

        self.viewport().stackUnder(self.frozenTableView)

        self.setShowGrid(True)

        hh = self.horizontalHeader()
        hh.setDefaultAlignment(Qt.AlignCenter)
        hh.setStretchLastSection(True)

        self.resizeColumnsToContents()

        vh = self.verticalHeader()
        vh.setDefaultSectionSize(25)
        vh.setDefaultAlignment(Qt.AlignCenter)
        vh.setVisible(True)
        self.frozenTableView.verticalHeader().setDefaultSectionSize(vh.defaultSectionSize())

        self.frozenTableView.show()
        self.updateFrozenTableGeometry()

        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.frozenTableView.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # connect the headers and scrollbars of both table view's together
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.frozenTableView.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.frozenTableView.verticalScrollBar().setValue)

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

    @property
    def fixed_col_count(self):
        return self._fixed_col_count

    @fixed_col_count.setter
    def fixed_col_count(self, value):
        self._fixed_col_count = value

    def update_view(self, simulator):
        data_copy = deepcopy(simulator.pipeline.stage_information)
        data_copy.insert(0, ["Instruction"] + [str(x) for x in list(range(len(data_copy[-1]) - 1))])
        self.model = TableModel(data_copy)
        QTableView.setModel(self, self.model)
        self.frozenTableView.setModel(self.model)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.setFocusPolicy(Qt.NoFocus)

        cols = self.model.columnCount(self.model)
        for col in range(cols):
            if col not in range(self._fixed_col_count):
                self.frozenTableView.setColumnHidden(col, True)
            else:
                self.frozenTableView.setColumnWidth(col, self.columnWidth(col))

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        self.scrollToBottom()
        self.horizontalScrollBar().setValue(self.horizontalScrollBar().maximum())

    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        if logicalIndex in range(self._fixed_col_count):
            self.frozenTableView.setColumnWidth(logicalIndex, newSize)
            self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self, event):
        QTableView.resizeEvent(self, event)
        self.updateFrozenTableGeometry()

    def scrollTo(self, index, hint):
        if index.column() >= self._fixed_col_count:
            QTableView.scrollTo(self, index, hint)

    def updateFrozenTableGeometry(self):
        frozen_width = sum([self.frozenTableView.columnWidth(col) for col in range(self._fixed_col_count)])
        frozen_height = sum([self.frozenTableView.rowHeight(row) for row in range(self._fixed_row_count)])
        self.frozenTableView.verticalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        if self.verticalHeader().isVisible():
            self.frozenTableView.setGeometry(self.verticalHeader().width() + self.frameWidth(),
                                             self.frameWidth(), frozen_width,
                                             self.viewport().height() + self.horizontalHeader().height())
        else:
            self.frozenTableView.setGeometry(self.frameWidth(),
                                             self.frameWidth(), frozen_width,
                                             self.viewport().height() + self.horizontalHeader().height())



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

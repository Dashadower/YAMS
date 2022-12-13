import xlrd

excel = xlrd.open_workbook("layout.xls", formatting_info=True)

sheet = excel.sheet_by_name("Components")

with open("pipeline_objects.py", "w") as f:
    imports = """
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
"""
    f.write(imports)
    for crange in sheet.merged_cells:
        y1, y2, x1, x2 = crange
        print(x1,x2, y1, y2)
        print(sheet.cell_value(y1, x1))

        template = f"""
class {sheet.cell_value(y1, x1)}Obj(QGraphicsRectItem):
    def __init__(self, scale_factor: int):
        # x y w h
        super().__init__({x1} * scale_factor, {y1} * scale_factor, {x2-x1} * scale_factor, {y2 - y1} * scale_factor)

        pen = QPen(Qt.black, 2)
        self.setPen(pen)
        self.text = QGraphicsSimpleTextItem("{sheet.cell_value(y1, x1)}", self)
        rect = self.text.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.text.setPos(rect.topLeft())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("clicked from", self)
        else:
            super().mousePressEvent(event)
    

"""
        f.write(template)
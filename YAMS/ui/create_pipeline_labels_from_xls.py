import xlrd

excel = xlrd.open_workbook("layout.xls", formatting_info=True)

sheet = excel.sheet_by_name("Labels")

search_range = [1, 100, 1, 40]  # xmin, xmax, ymin, ymax

with open("pipeline_labels.py", "w") as f:
    f.write("value_label_brush = QBrush(Qt.red)\n")
    merged_cells = set()
    for (y1, y2, x1, x2) in sheet.merged_cells:
        for x in range(x1, x2):
            for y in range(y1, y2):
                merged_cells.add((x, y))



    for row in range(search_range[2], search_range[3] + 1):
        for col in range(search_range[0], search_range[1] + 1):
            if (col, row) in merged_cells:
                continue
            try:
                if sheet.cell_value(row, col):
                    name = sheet.cell_value(row, col)
                    template = f"""
self.{name}_label = QGraphicsSimpleTextItem()
self.{name}_label.setBrush(value_label_brush)
self.{name}_label.setPos(self.object_scale_factor * {col}, self.object_scale_factor * {row})
self.{name}_label.setText("{name}")
self.scene.addItem(self.{name}_label)

"""
                    f.write(template)
            except:
                pass

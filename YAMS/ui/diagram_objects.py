

class DiagramComponent:
    def __init__(self, name=""):
        self.name = name
        self._qt_object = None

    def on_rising_edge(self):
        raise NotImplementedError

    def redraw(self):
        raise NotImplementedError


class DiagramNode(DiagramComponent):
    def __init__(self, name=""):
        super(DiagramNode, self).__init__(name)


class DiagramCircuitConnection(DiagramComponent):
    def __init__(self, from_node, to_node, name=""):
        super(DiagramCircuitConnection, self).__init__(name=name)
        self.value = ""
        self.from_node = from_node
        self.to_node = to_node

    def set_value(self, value: str):
        self.value = value

    def clear_value(self):
        self.value = ""

from kivy.uix.widget import Widget
from kivy.graphics import *


class FieldWidget(Widget):
    def __init__(self, **kwargs):
        super(FieldWidget, self).__init__(**kwargs)
        self.bind(pos=self.update_canvas)
        self.bind(size=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(0, 0), size=(10, 10))

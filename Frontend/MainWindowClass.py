from kivy.app import App

from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from FieldWidget import FieldWidget

Window.size = (604, 604)
Window.clearcolor = (0.2, 0.2, 0.2)


class PythonGameApp(App):
    def build(self):
        self.title = 'the Python game (v 2.0.0)'
        grid = GridLayout(cols=3)
        grid.add_widget(FieldWidget())
        grid.add_widget(Button())
        return grid


if __name__ == "__main__":
    PythonGameApp().run()

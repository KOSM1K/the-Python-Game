import threading

from kivy.app import App

from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from KeyboardCatcherWidget import KeyboardCatcherWidget
from BackEnd.ClockClass import Clock

Window.size = (604, 604)
Window.clearcolor = (0.2, 0.2, 0.2, 0.2)


class PythonGameApp(App):
    def build(self):
        global a
        self.title = 'the Python game (v 2.0.0)'
        self.icon = 'Textures\icon.png'
        grid = GridLayout(cols=3)
        grid.add_widget(KeyboardCatcherWidget())
        grid.add_widget(Button())
        return grid

    def on_stop(self):
        pass


if __name__ == "__main__":
    PythonGameApp().run()

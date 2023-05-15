from kivy.app import App

from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

from VisualField import FieldWidget

Window.size = (604, 604)
Window.clearcolor = (0.2, 0.2, 0.2)



class PyGameApp(App):
    def build(self):
        self.title = 'the Python game (v 2.0.0)'
        box = BoxLayout()
        btn = Button(text='жми!')
        label = Label(text='aboba')
        box.add_widget(btn)
        box.add_widget(label)
        # box.add_widget(FieldWidget)

        return FieldWidget()


if __name__ == "__main__":
    PyGameApp().run()

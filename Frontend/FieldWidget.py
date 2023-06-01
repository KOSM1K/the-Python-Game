from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import *


class FieldWidget(Widget):
    def __init__(self, **kwargs):
        super(FieldWidget, self).__init__(**kwargs)
        self.size_hint = None, None
        self.height = 0
        self.width = 0
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.bind(pos=self.update_picture)
        self.bind(size=self.update_picture)
        self.update_picture()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('down', keycode[1])
        self.size_hint = 50, 1

        return True

    def _on_keyboard_up(self, keyboard, keycode):
        print('up', keycode[1])

    def update_picture(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 0)
            Rectangle(pos=(self.pos[0] + 10, self.pos[1] + 10), size=(10, 10))

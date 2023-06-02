from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import *


class KeyboardCatcherWidget(Widget):
    def __init__(self, **kwargs):
        super(KeyboardCatcherWidget, self).__init__(**kwargs)

        # setting size to zero
        # enabling manual in-pixel size setting
        self.size_hint = None, None

        # setting size to zero
        self.height = 0
        self.width = 0

        # preparing for keyboard capture
        # getting keyboard object
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        # binding functions to actions
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

        # list that contains all pressed buttons
        self.__pressedKeys__ = []
        # bool that indicates changes of pressed keys
        self.__keysChanged__ = False

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] not in self.__pressedKeys__:
            self.__pressedKeys__.append(keycode[1])
            self.__keysChanged__ = True
            call(self)

    def _on_keyboard_up(self, keyboard, keycode):
        self.__pressedKeys__.remove(keycode[1])
        self.__keysChanged__ = True
        call(self)

    def pressedKeys(self):
        result = self.__keysChanged__, self.__pressedKeys__
        self.__keysChanged__ = False
        return result


def call(a: KeyboardCatcherWidget):
    result = a.pressedKeys()
    if result[0]: print(result[1])

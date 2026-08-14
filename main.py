from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.core.window import Window


class RoundedButton(Button):
    def __init__(self, bg_color=(0.12, 0.13, 0.17, 1), **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self.bg_color = bg_color

        with self.canvas.before:
            self.color_instruction = Color(*self.bg_color)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(18)]
            )

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class Calculator(App):

    def build(self):

        Window.clearcolor = (0.04, 0.045, 0.06, 1)

        root = BoxLayout(
            orientation="vertical",
            padding=[dp(14), dp(18), dp(14), dp(14)],
            spacing=dp(12)
        )

        # ---------------- DISPLAY ----------------

        display_box = BoxLayout(
            orientation="vertical",
            size_hint_y=0.28,
            padding=[dp(18), dp(12)]
        )

        with display_box.canvas.before:
            Color(0.08, 0.09, 0.12, 1)
            display_rect = RoundedRectangle(
                pos=display_box.pos,
                size=display_box.size,
                radius=[dp(24)]
            )

        display_box.bind(
            pos=lambda obj, value: setattr(display_rect, "pos", value),
            size=lambda obj, value: setattr(display_rect, "size", value)
        )

        self.display = Label(
            text="0",
            font_size=dp(42),
            color=(1, 1, 1, 1),
            halign="right",
            valign="middle",
            text_size=(None, None)
        )

        display_box.add_widget(self.display)
        root.add_widget(display_box)

        # ---------------- BUTTONS ----------------

        buttons = GridLayout(
            cols=4,
            spacing=dp(10),
            size_hint_y=0.72
        )

        button_data = [
            ("C", "clear"),
            ("⌫", "back"),
            ("÷", "/"),
            ("×", "*"),

            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("−", "-"),

            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("+", "+"),

            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("=", "="),

            ("0", "0"),
            (".", "."),
            ("%", "%"),
            ("±", "sign"),
        ]

        for text, value in button_data:

            if value in ["+", "-", "*", "/", "="]:
                color = (0.35, 0.20, 0.75, 1)

            elif value in ["clear", "back", "%", "sign"]:
                color = (0.18, 0.20, 0.25, 1)

            else:
                color = (0.11, 0.12, 0.16, 1)

            btn = RoundedButton(
                text=text,
                font_size=dp(24),
                color=(1, 1, 1, 1),
                bg_color=color
            )

            btn.bind(
                on_release=lambda instance, v=value:
                self.press(v)
            )

            buttons.add_widget(btn)

        root.add_widget(buttons)

        self.current = ""

        return root

    # ---------------- CALCULATOR LOGIC ----------------

    def press(self, value):

        if value == "clear":
            self.current = ""
            self.display.text = "0"
            return

        if value == "back":
            self.current = self.current[:-1]

            if self.current:
                self.display.text = self.current
            else:
                self.display.text = "0"

            return

        if value == "sign":

            if self.current:

                if self.current.startswith("-"):
                    self.current = self.current[1:]
                else:
                    self.current = "-" + self.current

                self.display.text = self.current

            return

        if value == "=":

            try:
                expression = self.current

                expression = expression.replace("%", "/100")

                result = eval(
                    expression,
                    {"__builtins__": None},
                    {}
                )

                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 10)

                self.current = str(result)
                self.display.text = str(result)

            except Exception:
                self.display.text = "Error"
                self.current = ""

            return

        # Prevent multiple operators together

        if value in ["+", "-", "*", "/"]:

            if not self.current:
                if value == "-":
                    self.current = "-"
                    self.display.text = "-"
                return

            if self.current[-1] in ["+", "-", "*", "/"]:
                self.current = self.current[:-1]

            self.current += value
            self.display.text = self.current
            return

        # Decimal protection

        if value == ".":

            last_number = self.current

            for op in ["+", "-", "*", "/"]:
                last_number = last_number.split(op)[-1]

            if "." in last_number:
                return

        self.current += value
        self.display.text = self.current


if __name__ == "__main__":
    Calculator().run()

import math

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle


class CalcButton(Button):
    def __init__(self, bg=(0.12, 0.13, 0.17, 1), **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before:
            Color(*bg)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(15)]
            )

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class CalculatorApp(App):

    def build(self):

        self.expression = ""
        self.degree = True

        root = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        # Display
        self.display = Label(
            text="0",
            font_size=dp(38),
            color=(1, 1, 1, 1),
            halign="right",
            valign="middle",
            size_hint_y=0.22
        )

        with self.display.canvas.before:
            Color(0.07, 0.08, 0.11, 1)
            self.display_bg = RoundedRectangle(
                pos=self.display.pos,
                size=self.display.size,
                radius=[dp(20)]
            )

        self.display.bind(
            pos=self.update_display_bg,
            size=self.update_display_bg
        )

        root.add_widget(self.display)

        # Mode
        self.mode_button = CalcButton(
            text="DEG",
            font_size=dp(16),
            bg=(0.35, 0.20, 0.70, 1),
            size_hint_y=0.08
        )

        self.mode_button.bind(
            on_release=self.change_mode
        )

        root.add_widget(self.mode_button)

        # Buttons
        grid = GridLayout(
            cols=4,
            spacing=dp(8),
            size_hint_y=0.70
        )

        buttons = [
            ("AC", "AC"),
            ("⌫", "BACK"),
            ("√", "SQRT"),
            ("x²", "SQUARE"),

            ("sin", "SIN"),
            ("cos", "COS"),
            ("tan", "TAN"),
            ("π", "PI"),

            ("7", "7"),
            ("8", "8"),
            ("9", "9"),
            ("÷", "/"),

            ("4", "4"),
            ("5", "5"),
            ("6", "6"),
            ("×", "*"),

            ("1", "1"),
            ("2", "2"),
            ("3", "3"),
            ("−", "-"),

            ("0", "0"),
            (".", "."),
            ("%", "%"),
            ("+", "+"),

            ("(", "("),
            (")", ")"),
            ("±", "SIGN"),
            ("=", "=")
        ]

        for text, value in buttons:

            if value in ["+", "-", "*", "/", "="]:
                color = (0.35, 0.20, 0.70, 1)

            elif value in [
                "AC", "BACK", "SQRT",
                "SQUARE", "SIN", "COS",
                "TAN", "PI", "SIGN"
            ]:
                color = (0.16, 0.18, 0.23, 1)

            else:
                color = (0.10, 0.11, 0.15, 1)

            btn = CalcButton(
                text=text,
                font_size=dp(20),
                color=(1, 1, 1, 1),
                bg=color
            )

            btn.bind(
                on_release=lambda instance, v=value:
                self.press(v)
            )

            grid.add_widget(btn)

        root.add_widget(grid)

        return root

    def update_display_bg(self, *args):
        self.display_bg.pos = self.display.pos
        self.display_bg.size = self.display.size

    def change_mode(self, instance):

        self.degree = not self.degree

        if self.degree:
            instance.text = "DEG"
        else:
            instance.text = "RAD"

    def press(self, value):

        if value == "AC":
            self.expression = ""
            self.display.text = "0"
            return

        if value == "BACK":
            self.expression = self.expression[:-1]
            self.show()
            return

        if value == "PI":
            self.expression += str(math.pi)
            self.show()
            return

        if value == "SQRT":
            self.expression += "sqrt("
            self.show()
            return

        if value == "SQUARE":
            self.expression += "**2"
            self.show()
            return

        if value == "SIN":
            self.expression += "sin("
            self.show()
            return

        if value == "COS":
            self.expression += "cos("
            self.show()
            return

        if value == "TAN":
            self.expression += "tan("
            self.show()
            return

        if value == "SIGN":

            if self.expression:
                if self.expression.startswith("-"):
                    self.expression = self.expression[1:]
                else:
                    self.expression = "-" + self.expression

                self.show()

            return

        if value == "=":
            self.calculate()
            return

        self.expression += value
        self.show()

    def show(self):

        text = self.expression

        text = text.replace("*", "×")
        text = text.replace("/", "÷")

        self.display.text = text if text else "0"

    def calculate(self):

        if not self.expression:
            return

        try:

            expr = self.expression

            expr = expr.replace("sqrt", "math.sqrt")

            # Trigonometry
            if self.degree:

                expr = expr.replace(
                    "sin(",
                    "math.sin(math.radians("
                )

                expr = expr.replace(
                    "cos(",
                    "math.cos(math.radians("
                )

                expr = expr.replace(
                    "tan(",
                    "math.tan(math.radians("
                )

                # Each trig function needs one extra )
                expr = self.close_trig(expr)

            else:

                expr = expr.replace(
                    "sin(",
                    "math.sin("
                )

                expr = expr.replace(
                    "cos(",
                    "math.cos("
                )

                expr = expr.replace(
                    "tan(",
                    "math.tan("
                )

            # Percentage
            expr = expr.replace("%", "/100")

            result = eval(
                expr,
                {
                    "__builtins__": {},
                    "math": math
                }
            )

            if isinstance(result, float):

                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 8)

            self.expression = str(result)
            self.display.text = str(result)

        except Exception:
            self.display.text = "Error"
            self.expression = ""

    def close_trig(self, expr):

        functions = [
            "math.sin(math.radians(",
            "math.cos(math.radians(",
            "math.tan(math.radians("
        ]

        for function in functions:

            while function in expr:

                start = expr.find(function)

                pos = start + len(function)

                depth = 0

                while pos < len(expr):

                    if expr[pos] == "(":
                        depth += 1

                    elif expr[pos] == ")":

                        if depth == 0:
                            break

                        depth -= 1

                    pos += 1

                expr = (
                    expr[:pos + 1]
                    + ")"
                    + expr[pos + 1:]
                )

                break

        return expr


if __name__ == "__main__":
    CalculatorApp().run()

import math
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle


class CalcButton(Button):
    def __init__(self, bg, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before:
            Color(*bg)
            self.shape = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(14)]
            )

        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        self.shape.pos = self.pos
        self.shape.size = self.size


class CalculatorApp(App):

    def build(self):
        self.expression = ""
        self.answer = 0
        self.history = []
        self.degree_mode = True

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(8)
        )

        # ---------------- DISPLAY ----------------

        display = BoxLayout(
            orientation="vertical",
            size_hint_y=0.22,
            padding=dp(14)
        )

        with display.canvas.before:
            Color(0.06, 0.07, 0.10, 1)
            self.display_bg = RoundedRectangle(
                pos=display.pos,
                size=display.size,
                radius=[dp(20)]
            )

        display.bind(
            pos=self.update_display_bg,
            size=self.update_display_bg
        )

        self.history_text = Label(
            text="",
            font_size=dp(13),
            color=(0.55, 0.60, 0.68, 1),
            halign="right",
            valign="middle"
        )

        self.screen = Label(
            text="0",
            font_size=dp(34),
            color=(1, 1, 1, 1),
            halign="right",
            valign="middle"
        )

        display.add_widget(self.history_text)
        display.add_widget(self.screen)

        root.add_widget(display)

        # ---------------- MODE BAR ----------------

        mode = BoxLayout(
            size_hint_y=0.07,
            spacing=dp(6)
        )

        self.mode_btn = CalcButton(
            (0.36, 0.20, 0.70, 1),
            text="DEG",
            font_size=dp(14)
        )

        self.mode_btn.bind(
            on_release=self.change_mode
        )

        hist_btn = CalcButton(
            (0.14, 0.16, 0.21, 1),
            text="HISTORY",
            font_size=dp(13)
        )

        hist_btn.bind(
            on_release=self.show_history
        )

        mode.add_widget(self.mode_btn)
        mode.add_widget(hist_btn)

        root.add_widget(mode)

        # ---------------- BUTTONS ----------------

        grid = GridLayout(
            cols=5,
            spacing=dp(6),
            size_hint_y=0.71
        )

        buttons = [
            ("AC", "AC", "danger"),
            ("⌫", "BACK", "func"),
            ("(", "(", "func"),
            (")", ")", "func"),
            ("%", "%", "func"),

            ("sin", "sin", "func"),
            ("cos", "cos", "func"),
            ("tan", "tan", "func"),
            ("√", "sqrt", "func"),
            ("x²", "square", "func"),

            ("asin", "asin", "func"),
            ("acos", "acos", "func"),
            ("atan", "atan", "func"),
            ("log", "log", "func"),
            ("ln", "ln", "func"),

            ("π", "pi", "func"),
            ("e", "e", "func"),
            ("xʸ", "^", "func"),
            ("1/x", "inverse", "func"),
            ("!", "factorial", "func"),

            ("7", "7", "num"),
            ("8", "8", "num"),
            ("9", "9", "num"),
            ("÷", "/", "op"),
            ("×", "*", "op"),

            ("4", "4", "num"),
            ("5", "5", "num"),
            ("6", "6", "num"),
            ("−", "-", "op"),
            ("+", "+", "op"),

            ("1", "1", "num"),
            ("2", "2", "num"),
            ("3", "3", "num"),
            (".", ".", "num"),
            ("=", "=", "equal"),

            ("0", "0", "num"),
            ("00", "00", "num"),
            ("±", "sign", "func"),
            ("ANS", "ans", "func"),
            ("EXP", "exp", "func"),
        ]

        colors = {
            "num": (0.10, 0.11, 0.15, 1),
            "func": (0.15, 0.17, 0.23, 1),
            "op": (0.34, 0.19, 0.68, 1),
            "equal": (0.10, 0.50, 0.82, 1),
            "danger": (0.62, 0.15, 0.20, 1)
        }

        for text, value, kind in buttons:

            button = CalcButton(
                colors[kind],
                text=text,
                font_size=dp(16),
                color=(1, 1, 1, 1)
            )

            button.bind(
                on_release=lambda instance, v=value:
                self.press(v)
            )

            grid.add_widget(button)

        root.add_widget(grid)

        return root

    # ---------------- DISPLAY ----------------

    def update_display_bg(self, *args):
        self.display_bg.pos = args[1]
        self.display_bg.size = args[2]

    def show(self):
        text = self.expression
        text = text.replace("*", "×")
        text = text.replace("/", "÷")
        self.screen.text = text if text else "0"

    # ---------------- MODE ----------------

    def change_mode(self, instance):

        self.degree_mode = not self.degree_mode

        instance.text = (
            "DEG" if self.degree_mode else "RAD"
        )

    # ---------------- BUTTON PRESS ----------------

    def press(self, value):

        if value == "AC":
            self.expression = ""
            self.screen.text = "0"
            self.history_text.text = ""
            return

        if value == "BACK":
            self.expression = self.expression[:-1]
            self.show()
            return

        if value == "=":
            self.calculate()
            return

        if value == "ans":
            self.expression += str(self.answer)
            self.show()
            return

        if value == "sign":
            self.toggle_sign()
            return

        if value == "pi":
            self.expression += "pi"
            self.show()
            return

        if value == "e":
            self.expression += "e"
            self.show()
            return

        if value == "sqrt":
            self.expression += "sqrt("
            self.show()
            return

        if value == "square":
            self.expression += "^2"
            self.show()
            return

        if value == "inverse":
            self.expression += "inv("
            self.show()
            return

        if value == "factorial":
            self.expression += "!"
            self.show()
            return

        if value == "exp":
            self.expression += "*10^"
            self.show()
            return

        functions = [
            "sin", "cos", "tan",
            "asin", "acos", "atan",
            "log", "ln"
        ]

        if value in functions:
            self.expression += value + "("
            self.show()
            return

        self.expression += value
        self.show()

    # ---------------- SIGN ----------------

    def toggle_sign(self):

        if not self.expression:
            return

        if self.expression.startswith("-"):
            self.expression = self.expression[1:]
        else:
            self.expression = "-" + self.expression

        self.show()

    # ---------------- CALCULATION ----------------

    def calculate(self):

        if not self.expression:
            return

        try:

            original = self.expression

            expr = original

            # Power
            expr = expr.replace("^", "**")

            # Constants
            expr = expr.replace("pi", "math.pi")

            # Square root
            expr = expr.replace("sqrt", "math.sqrt")

            # Log
            expr = expr.replace("log", "math.log10")
            expr = expr.replace("ln", "math.log")

            # Percentage
            expr = expr.replace("%", "/100")

            # Factorial
            expr = self.replace_factorial(expr)

            # Inverse
            expr = self.replace_inverse(expr)

            # Trigonometry
            expr = self.convert_trigonometry(expr)

            result = eval(
                expr,
                {
                    "__builtins__": {},
                    "math": math
                }
            )

            if isinstance(result, float):

                if abs(result) < 1e-12:
                    result = 0

                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            self.answer = result

            self.history.append(
                (original, result)
            )

            self.history_text.text = (
                original + " ="
            )

            self.screen.text = str(result)

            self.expression = str(result)

        except Exception:

            self.screen.text = "Error"
            self.expression = ""

    # ---------------- TRIGONOMETRY ----------------

    def convert_trigonometry(self, expr):

        funcs = [
            "sin",
            "cos",
            "tan",
            "asin",
            "acos",
            "atan"
        ]

        for func in funcs:

            target = func + "("

            while target in expr:

                start = expr.find(target)

                open_pos = start + len(func)

                end = self.find_close(
                    expr,
                    open_pos
                )

                if end == -1:
                    raise ValueError()

                inside = expr[
                    open_pos + 1:end
                ]

                if func in ["sin", "cos", "tan"]:

                    if self.degree_mode:

                        replacement = (
                            "math."
                            + func
                            + "(math.radians("
                            + inside
                            + "))"
                        )

                    else:

                        replacement = (
                            "math."
                            + func
                            + "("
                            + inside
                            + ")"
                        )

                else:

                    if self.degree_mode:

                        replacement = (
                            "math.degrees("
                            "math."
                            + func
                            + "("
                            + inside
                            + "))"
                        )

                    else:

                        replacement = (
                            "math."
                            + func
                            + "("
                            + inside
                            + ")"
                        )

                expr = (
                    expr[:start]
                    + replacement
                    + expr[end + 1:]
                )

        return expr

    def find_close(self, text, open_pos):

        depth = 0

        for i in range(
            open_pos + 1,
            len(text)
        ):

            if text[i] == "(":
                depth += 1

            elif text[i] == ")":

                if depth == 0:
                    return i

                depth -= 1

        return -1

    # ---------------- FACTORIAL ----------------

    def replace_factorial(self, expr):

        while "!" in expr:

            pos = expr.find("!")

            start = pos - 1

            while start >= 0 and (
                expr[start].isdigit()
            ):
                start -= 1

            number = expr[start + 1:pos]

            if not number:
                raise ValueError()

            value = math.factorial(
                int(number)
            )

            expr = (
                expr[:start + 1]
                + str(value)
                + expr[pos + 1:]
            )

        return expr

    # ---------------- INVERSE ----------------

    def replace_inverse(self, expr):

        while "inv(" in expr:

            start = expr.find("inv(")

            open_pos = start + 3

            end = self.find_close(
                expr,
                open_pos
            )

            if end == -1:
                raise ValueError()

            inside = expr[
                open_pos + 1:end
            ]

            replacement = (
                "(1/("
                + inside
                + "))"
            )

            expr = (
                expr[:start]
                + replacement
                + expr[end + 1:]
            )

        return expr

    # ---------------- HISTORY ----------------

    def show_history(self, instance):

        if not self.history:

            self.history_text.text = (
                "No history"
            )

            return

        recent = self.history[-4:]

        text = " | ".join(
            str(x) + "=" + str(y)
            for x, y in recent
        )

        self.history_text.text = text


if __name__ == "__main__":
    CalculatorApp().run()

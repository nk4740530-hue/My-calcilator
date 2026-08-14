import math

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle


class CalcButton(Button):

    def __init__(self, bg=(0.1, 0.1, 0.15, 1), **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        with self.canvas.before:
            Color(*bg)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(12)]
            )

        self.bind(
            pos=self.update_rect,
            size=self.update_rect
        )

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class CalculatorApp(App):

    def build(self):

        self.expression = ""
        self.answer = 0
        self.degree_mode = True
        self.history = []

        root = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(7)
        )

        # ---------------- DISPLAY ----------------

        display_box = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(3),
            size_hint_y=0.20
        )

        with display_box.canvas.before:
            Color(0.055, 0.065, 0.09, 1)
            self.display_rect = RoundedRectangle(
                pos=display_box.pos,
                size=display_box.size,
                radius=[dp(18)]
            )

        display_box.bind(
            pos=self.update_display,
            size=self.update_display
        )

        self.history_label = Label(
            text="",
            font_size=dp(12),
            color=(0.55, 0.60, 0.70, 1),
            halign="right",
            valign="middle"
        )

        self.screen = Label(
            text="0",
            font_size=dp(30),
            color=(1, 1, 1, 1),
            halign="right",
            valign="middle"
        )

        display_box.add_widget(self.history_label)
        display_box.add_widget(self.screen)

        root.add_widget(display_box)

        # ---------------- MODE ----------------

        mode_box = BoxLayout(
            size_hint_y=0.065,
            spacing=dp(6)
        )

        self.mode_button = CalcButton(
            (0.35, 0.18, 0.68, 1),
            text="DEG",
            font_size=dp(14)
        )

        self.mode_button.bind(
            on_release=self.change_mode
        )

        history_button = CalcButton(
            (0.13, 0.15, 0.20, 1),
            text="HISTORY",
            font_size=dp(12)
        )

        history_button.bind(
            on_release=self.show_history
        )

        mode_box.add_widget(self.mode_button)
        mode_box.add_widget(history_button)

        root.add_widget(mode_box)

        # ---------------- BUTTON GRID ----------------

        grid = GridLayout(
            cols=5,
            spacing=dp(5),
            size_hint_y=0.735
        )

        buttons = [

            ("AC", "AC", "danger"),
            ("⌫", "BACK", "function"),
            ("(", "(", "function"),
            (")", ")", "function"),
            ("%", "%", "function"),

            ("sin", "sin", "function"),
            ("cos", "cos", "function"),
            ("tan", "tan", "function"),
            ("√", "sqrt", "function"),
            ("x²", "square", "function"),

            ("asin", "asin", "function"),
            ("acos", "acos", "function"),
            ("atan", "atan", "function"),
            ("log", "log", "function"),
            ("ln", "ln", "function"),

            ("π", "pi", "function"),
            ("e", "e", "function"),
            ("xʸ", "^", "function"),
            ("1/x", "inverse", "function"),
            ("!", "factorial", "function"),

            ("7", "7", "number"),
            ("8", "8", "number"),
            ("9", "9", "number"),
            ("÷", "/", "operator"),
            ("×", "*", "operator"),

            ("4", "4", "number"),
            ("5", "5", "number"),
            ("6", "6", "number"),
            ("−", "-", "operator"),
            ("+", "+", "operator"),

            ("1", "1", "number"),
            ("2", "2", "number"),
            ("3", "3", "number"),
            (".", ".", "number"),
            ("=", "=", "equal"),

            ("0", "0", "number"),
            ("00", "00", "number"),
            ("±", "sign", "function"),
            ("ANS", "ans", "function"),
            ("EXP", "exp", "function")
        ]

        colors = {

            "number":
                (0.09, 0.10, 0.14, 1),

            "function":
                (0.14, 0.16, 0.21, 1),

            "operator":
                (0.34, 0.18, 0.68, 1),

            "equal":
                (0.08, 0.48, 0.82, 1),

            "danger":
                (0.62, 0.14, 0.19, 1)
        }

        for text, value, kind in buttons:

            button = CalcButton(
                colors[kind],
                text=text,
                font_size=dp(15),
                color=(1, 1, 1, 1)
            )

            button.bind(
                on_release=lambda instance, v=value:
                self.press(v)
            )

            grid.add_widget(button)

        root.add_widget(grid)

        return root

    # ---------------- DISPLAY BACKGROUND ----------------

    def update_display(self, instance, value):

        self.display_rect.pos = instance.pos
        self.display_rect.size = instance.size

    # ---------------- MODE ----------------

    def change_mode(self, instance):

        self.degree_mode = not self.degree_mode

        if self.degree_mode:
            instance.text = "DEG"
        else:
            instance.text = "RAD"

    # ---------------- SHOW EXPRESSION ----------------

    def show_expression(self):

        text = self.expression

        text = text.replace("*", "×")
        text = text.replace("/", "÷")

        if text:
            self.screen.text = text
        else:
            self.screen.text = "0"

    # ---------------- BUTTON PRESS ----------------

    def press(self, value):

        # Clear
        if value == "AC":

            self.expression = ""
            self.screen.text = "0"
            self.history_label.text = ""

            return

        # Backspace
        if value == "BACK":

            self.expression = self.expression[:-1]

            self.show_expression()

            return

        # Equals
        if value == "=":

            self.calculate()

            return

        # Previous answer
        if value == "ans":

            self.expression += str(self.answer)

            self.show_expression()

            return

        # Positive / Negative
        if value == "sign":

            if not self.expression:
                return

            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression

            self.show_expression()

            return

        # Pi
        if value == "pi":

            self.expression += "pi"

            self.show_expression()

            return

        # Euler number
        if value == "e":

            self.expression += "e"

            self.show_expression()

            return

        # Square root
        if value == "sqrt":

            self.expression += "sqrt("

            self.show_expression()

            return

        # Square
        if value == "square":

            self.expression += "^2"

            self.show_expression()

            return

        # Inverse
        if value == "inverse":

            self.expression += "inv("

            self.show_expression()

            return

        # Factorial
        if value == "factorial":

            self.expression += "!"

            self.show_expression()

            return

        # Scientific notation
        if value == "exp":

            self.expression += "*10^"

            self.show_expression()

            return

        # Functions
        functions = [
            "sin",
            "cos",
            "tan",
            "asin",
            "acos",
            "atan",
            "log",
            "ln"
        ]

        if value in functions:

            self.expression += value + "("

            self.show_expression()

            return

        # Normal button
        self.expression += value

        self.show_expression()

    # ---------------- CALCULATE ----------------

    def calculate(self):

        if not self.expression:
            return

        try:

            original = self.expression

            expression = original

            # Power
            expression = expression.replace(
                "^",
                "**"
            )

            # Pi
            expression = expression.replace(
                "pi",
                "math.pi"
            )

            # Euler number
            expression = expression.replace(
                "e",
                "math.e"
            )

            # Square root
            expression = expression.replace(
                "sqrt",
                "math.sqrt"
            )

            # Log10
            expression = expression.replace(
                "log",
                "math.log10"
            )

            # Natural log
            expression = expression.replace(
                "ln",
                "math.log"
            )

            # Percentage
            expression = expression.replace(
                "%",
                "/100"
            )

            # Factorial
            expression = self.convert_factorial(
                expression
            )

            # Inverse
            expression = self.convert_inverse(
                expression
            )

            # Trigonometry
            expression = self.convert_trigonometry(
                expression
            )

            result = eval(
                expression,
                {
                    "__builtins__": {},
                    "math": math
                }
            )

            # Clean result
            if isinstance(result, float):

                if abs(result) < 1e-12:
                    result = 0

                elif result.is_integer():
                    result = int(result)

                else:
                    result = round(
                        result,
                        10
                    )

            self.answer = result

            self.history.append(
                (original, result)
            )

            self.history_label.text = (
                original + " ="
            )

            self.screen.text = str(result)

            self.expression = str(result)

        except Exception:

            self.screen.text = "Error"

            self.expression = ""

    # ---------------- FIND CLOSING BRACKET ----------------

    def find_closing(
        self,
        text,
        opening_position
    ):

        depth = 0

        for i in range(
            opening_position + 1,
            len(text)
        ):

            if text[i] == "(":

                depth += 1

            elif text[i] == ")":

                if depth == 0:

                    return i

                depth -= 1

        return -1

    # ---------------- TRIG FUNCTIONS ----------------

    def convert_trigonometry(
        self,
        expression
    ):

        functions = [
            "sin",
            "cos",
            "tan",
            "asin",
            "acos",
            "atan"
        ]

        for function in functions:

            target = function + "("

            while target in expression:

                start = expression.find(
                    target
                )

                opening = start + len(function)

                closing = self.find_closing(
                    expression,
                    opening
                )

                if closing == -1:
                    raise ValueError()

                inside = expression[
                    opening + 1:
                    closing
                ]

                # Normal trig
                if function in [
                    "sin",
                    "cos",
                    "tan"
                ]:

                    if self.degree_mode:

                        replacement = (
                            "math."
                            + function
                            + "(math.radians("
                            + inside
                            + "))"
                        )

                    else:

                        replacement = (
                            "math."
                            + function
                            + "("
                            + inside
                            + ")"
                        )

                # Inverse trig
                else:

                    if self.degree_mode:

                        replacement = (
                            "math.degrees("
                            "math."
                            + function
                            + "("
                            + inside
                            + "))"
                        )

                    else:

                        replacement = (
                            "math."
                            + function
                            + "("
                            + inside
                            + ")"
                        )

                expression = (
                    expression[:start]
                    + replacement
                    + expression[closing + 1:]
                )

        return expression

    # ---------------- FACTORIAL ----------------

    def convert_factorial(
        self,
        expression
    ):

        while "!" in expression:

            position = expression.find("!")

            start = position - 1

            while (
                start >= 0
                and expression[start].isdigit()
            ):

                start -= 1

            number = expression[
                start + 1:
                position
            ]

            if not number:
                raise ValueError()

            result = math.factorial(
                int(number)
            )

            expression = (
                expression[:start + 1]
                + str(result)
                + expression[position + 1:]
            )

        return expression

    # ---------------- INVERSE ----------------

    def convert_inverse(
        self,
        expression
    ):

        while "inv(" in expression:

            start = expression.find(
                "inv("
            )

            opening = start + 3

            closing = self.find_closing(
                expression,
                opening
            )

            if closing == -1:
                raise ValueError()

            inside = expression[
                opening + 1:
                closing
            ]

            replacement = (
                "(1/("
                + inside
                + "))"
            )

            expression = (
                expression[:start]
                + replacement
                + expression[closing + 1:]
            )

        return expression

    # ---------------- HISTORY ----------------

    def show_history(self, instance):

        if not self.history:

            self.history_label.text = (
                "No history"
            )

            return

        recent = self.history[-5:]

        text = " | ".join(
            str(expression)
            + " = "
            + str(result)
            for expression, result
            in recent
        )

        self.history_label.text = text


if __name__ == "__main__":
    CalculatorApp().run()

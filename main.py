from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class Calculator(App):

    def build(self):
        layout = BoxLayout(orientation="vertical")

        self.display = TextInput(
            text="",
            readonly=True,
            halign="right",
            font_size=40
        )
        layout.add_widget(self.display)

        buttons = [
            ["C", "⌫", "/", "*"],
            ["7", "8", "9", "-"],
            ["4", "5", "6", "+"],
            ["1", "2", "3", "="],
            ["0", ".", "%"]
        ]

        for row in buttons:
            row_layout = BoxLayout()

            for value in row:
                button = Button(
                    text=value,
                    font_size=28
                )
                button.bind(on_press=self.click)
                row_layout.add_widget(button)

            layout.add_widget(row_layout)

        return layout

    def click(self, button):
        value = button.text

        if value == "C":
            self.display.text = ""

        elif value == "⌫":
            self.display.text = self.display.text[:-1]

        elif value == "=":
            try:
                self.display.text = str(eval(self.display.text))
            except:
                self.display.text = "Error"

        elif value == "%":
            try:
                self.display.text = str(float(self.display.text) / 100)
            except:
                self.display.text = "Error"

        else:
            if self.display.text == "Error":
                self.display.text = ""
            self.display.text += value


Calculator().run()

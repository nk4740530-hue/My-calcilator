from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class Calculator(App):

    def build(self):
        layout = GridLayout(cols=4)

        self.display = TextInput(
            text="",
            readonly=True,
            font_size=35,
            halign="right"
        )

        layout.add_widget(self.display)

        buttons = [
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "C", "0", "=", "+"
        ]

        for text in buttons:
            button = Button(
                text=text,
                font_size=30
            )
            button.bind(on_press=self.button_pressed)
            layout.add_widget(button)

        return layout

    def button_pressed(self, instance):
        value = instance.text

        if value == "C":
            self.display.text = ""

        elif value == "=":
            try:
                self.display.text = str(
                    eval(self.display.text)
                )
            except:
                self.display.text = "Error"

        else:
            self.display.text += value


Calculator().run()

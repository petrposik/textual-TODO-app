from textual.app import App
from textual.widget import Widget
from textual.widgets import Button, Header, Footer, Input, Label


class LabelledInput(Widget):
    DEFAULT_CSS = """
    LabelledInput {
        height: 3;
    }
    """

    def __init__(self, label="Label", placeholder=None):
        super().__init__()
        self.label = label
        self.placeholder = placeholder or label.lower()

    def compose(self):
        yield Label(f"{self.label}: ")
        yield Input(placeholder=self.placeholder)


class TODOApp(App):
    BINDINGS = [
        ("b", "ring_bell", "Ring the bell"),
    ]

    def compose(self):
        yield Header(name="TODO App")
        yield LabelledInput("Name")
        yield LabelledInput("Surame")
        yield LabelledInput("Email")
        yield Button("Click me")
        yield Footer()

    def action_ring_bell(self):
        self.bell()
        self.mount(Label("Bell rang!"))


TODOApp().run()

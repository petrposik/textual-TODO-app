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


class TodoItem(Widget):
    DEFAULT_CSS = """
    TodoItem {
        height: 2;
    }
    """

    def __init__(self, description="Get this done!", due_date="yyyy-mm-dd"):
        super().__init__()
        self.description = description
        self.due_date = due_date

    def compose(self):
        yield Label(self.description)
        yield Label(self.due_date)


class TODOApp(App):
    BINDINGS = [
        ("b", "ring_bell", "Ring the bell"),
        ("n", "new_todo", "Create a new todo item"),
    ]

    def compose(self):
        yield Header(name="TODO App")
        yield Footer()

    def action_ring_bell(self):
        self.bell()

    def action_new_todo(self):
        self.mount(TodoItem())


TODOApp().run()

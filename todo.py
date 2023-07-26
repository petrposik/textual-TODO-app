from dataclasses import dataclass
from textual import on
from textual.app import App
from textual.containers import Horizontal
from textual.message import Message
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
        height: 3;
    }
    TodoItem Label {
        padding: 1;
        padding-left: 0;
    }
    """

    @dataclass
    class DeletionRequest(Message):
        widget_to_delete: "TodoItem"

    def __init__(self, description="Get this done!", due_date="yyyy-mm-dd"):
        super().__init__()
        self.description = description
        self.due_date = due_date

    def compose(self):
        with Horizontal():
            yield Label(self.description)
            yield Label(self.due_date)
            yield Button("Delete", id="delete")
            yield Button("Edit", id="edit")

    @on(Button.Pressed, "#delete")
    def delete(self):
        self.post_message(self.DeletionRequest(self))


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

    @on(TodoItem.DeletionRequest)
    def remove_todo(self, message):
        message.widget_to_delete.remove()


TODOApp().run()

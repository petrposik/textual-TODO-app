from dataclasses import dataclass
from functools import partial
from textual import on
from textual.app import App
from textual.containers import Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.screen import ModalScreen
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

    description = reactive("")
    date = reactive("")

    @dataclass
    class Delete(Message):
        item: "TodoItem"

    @dataclass
    class Edit(Message):
        item: "TodoItem"

    def __init__(self):
        super().__init__()
        self.description_label = Label()
        self.date_label = Label()

    def compose(self):
        with Horizontal():
            yield self.description_label
            yield self.date_label
            yield Button("Delete", id="delete")
            yield Button("Edit", id="edit")

    def watch_description(self, description):
        self.description_label.update(description)

    def watch_date(self, date):
        self.date_label.update(date)

    @on(Button.Pressed, "#delete")
    def delete(self):
        self.post_message(self.Delete(self))

    @on(Button.Pressed, "#edit")
    def edit(self):
        self.post_message(self.Edit(self))


class TodoItemDetailsScreen(ModalScreen):
    DEFAULT_CSS = """
    TodoItemDetailsScreen {
        align: center middle;
    }
    """

    def __init__(self, init_descr="Get it done!", init_date="yyyy-mm-dd"):
        super().__init__()
        self.description_input = Input(placeholder=init_descr)
        self.date_input = Input(placeholder=init_date)
        self.description_input.value = init_descr
        self.date_input.value = init_date

    def compose(self):
        yield Label("Description:")
        yield self.description_input
        yield Label("Date:")
        yield self.date_input
        yield Button("Submit")

    def on_button_pressed(self):
        data = (self.description_input.value, self.date_input.value)
        self.dismiss(data)


class TODOApp(App):
    BINDINGS = [
        ("b", "ring_bell", "Ring the bell"),
        ("n", "new_todo", "Create a new todo item"),
    ]

    def compose(self):
        yield Header(name="TODO App", show_clock=True)
        yield Footer()

    def action_ring_bell(self):
        self.bell()

    def action_new_todo(self):
        self.push_screen(TodoItemDetailsScreen(), self.new_todo_callback)

    def new_todo_callback(self, data):
        item = TodoItem()
        description, due_date = data
        item.description = description
        item.date = due_date
        self.mount(item)

    @on(TodoItem.Delete)
    def remove_todo(self, message):
        message.item.remove()

    @on(TodoItem.Edit)
    def edit_todo(self, message):
        self.push_screen(
            TodoItemDetailsScreen(message.item.description, message.item.date),
            partial(self.edit_todo_callback, message.item),
        )

    def edit_todo_callback(self, item, data):
        description, due_date = data
        item.description = description
        item.date = due_date


TODOApp().run()

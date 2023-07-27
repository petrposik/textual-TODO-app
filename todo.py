from dataclasses import dataclass
from functools import partial
from textual import on, work
from textual.app import App
from textual.containers import Horizontal, Center, Container
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
        height: 2;
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
        self.description_label = Label(id="description")
        self.date_label = Label(id="date")

    def compose(self):
        with Horizontal():
            yield Button("✅", classes="emoji-button", id="delete")
            yield Button("📝", classes="emoji-button", id="edit")
            yield self.description_label
            yield self.date_label

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

    def __init__(self, init_descr="", init_date=""):
        super().__init__()
        self.description_input = Input(placeholder="Get it done!")
        self.date_input = Input(placeholder="yyyy-mm-dd")
        self.description_input.value = init_descr
        self.date_input.value = init_date

    def compose(self):
        with Container():
            yield Label("Description:")
            yield self.description_input
            yield Label("Date:")
            yield self.date_input
            with Center():
                yield Button("Submit")

    def on_button_pressed(self):
        data = (self.description_input.value, self.date_input.value)
        self.dismiss(data)


class TODOApp(App):
    CSS_PATH = "todo.css"
    BINDINGS = [
        ("n", "new_todo", "Create a new todo item"),
        ("q", "quit", "Quit the application"),
    ]

    def compose(self):
        yield Header(name="TODO App", show_clock=True)
        yield Footer()

    def on_mount(self):
        self.load_todos()

    def load_todos(self):
        with open("todos.dsv") as f:
            for line in f:
                description, date = line.strip().split("|")
                item = TodoItem()
                item.description = description
                item.date = date
                self.mount(item)

    def action_quit(self):
        self.save_todos()
        self.exit()

    def save_todos(self):
        with open("todos.dsv", "w") as f:
            for item in self.query(TodoItem):
                f.write(f"{item.description}|{item.date}\n")

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

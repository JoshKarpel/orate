from __future__ import annotations

from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static

from spiel.renderables.debug import DebugTable
from spiel.widgets.footer import Footer


class HelpScreen(Screen):
    DEFAULT_CSS = """
    Screen {
        align: center middle;
    }

    .content-center {
        content-align: center middle;
    }
    """

    BINDINGS = [
        ("escape,enter", "pop_screen", "Close"),
    ]

    def compose(self) -> ComposeResult:
        yield Static(DebugTable(), classes="content-center")
        yield Footer()

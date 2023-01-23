from __future__ import annotations

from enum import Enum
from typing import Protocol

from textual.widget import Widget


class Direction(Enum):
    Right = "right"
    Left = "left"


class Transition(Protocol):
    def initialize(self, to_widget: Widget, direction: Direction) -> None:
        ...

    def progress(
        self,
        from_widget: Widget,
        to_widget: Widget,
        direction: Direction,
        progress: float,
    ) -> None:
        ...


class Swipe(Transition):
    def initialize(self, to_widget: Widget, direction: Direction) -> None:
        to_widget.styles.offset = ("100%" if direction is Direction.Right else "-100%", 0)

    def progress(
        self,
        from_widget: Widget,
        to_widget: Widget,
        direction: Direction,
        progress: float,
    ) -> None:
        match direction:
            case Direction.Right:
                from_widget.styles.offset = (f"-{progress:.1f}%", 0)
                to_widget.styles.offset = (f"{100 - progress:.1f}%", 0)
            case Direction.Left:
                from_widget.styles.offset = (f"{progress:.1f}%", 0)
                to_widget.styles.offset = (f"-{100 - progress:.1f}%", 0)

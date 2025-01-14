from rich.align import Align
from rich.console import Group, RenderableType
from rich.padding import Padding
from rich.style import Style
from rich.text import Text

from spiel import Deck, Triggers

deck = Deck(name="Trigger Examples")


@deck.slide(title="Revealing Content")
def reveal(triggers: Triggers) -> RenderableType:
    lines = [
        Text.from_markup(
            f"This slide has been triggered [yellow]{len(triggers)}[/yellow] time{'s' if len(triggers) > 1 else ''}."
        ),
        Text("First line.", style=Style(color="red")) if len(triggers) >= 1 else None,
        Text("Second line.", style=Style(color="blue")) if len(triggers) >= 2 else None,
        Text("Third line.", style=Style(color="green")) if len(triggers) >= 3 else None,
    ]

    return Group(
        *(Padding(Align.center(line), pad=(0, 0, 1, 0)) for line in lines if line is not None)
    )

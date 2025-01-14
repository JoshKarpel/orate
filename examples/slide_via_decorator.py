from rich.align import Align
from rich.console import RenderableType
from rich.text import Text

from spiel import Deck

deck = Deck(name="Deck Name")


@deck.slide(title="Slide Title")
def slide_content() -> RenderableType:
    return Align(
        Text.from_markup(
            "[blue]Your[/blue] [red underline]content[/red underline] [green italic]here[/green italic]!"
        ),
        align="center",
        vertical="middle",
    )

from math import floor

from rich.align import Align
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text

from spiel import Deck, Triggers

deck = Deck(name="Trigger Examples")


@deck.slide(title="Animating Content")
def animate(triggers: Triggers) -> RenderableType:
    bang = "!"
    space = " "
    bar_length = 5

    spaces_before_bang = min(floor(triggers.time_since_first_trigger), bar_length)
    spaces_after_bang = bar_length - spaces_before_bang

    bar = (space * spaces_before_bang) + bang + (space * spaces_after_bang)

    return Align(
        Group(
            Align.center(Text(f"{triggers=}")),
            Align.center(Text(f"{spaces_before_bang=} | {spaces_after_bang=}")),
            Align.center(Panel(Text(bar), expand=False, height=3)),
        ),
        align="center",
        vertical="middle",
    )

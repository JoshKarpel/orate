from rich.align import Align
from rich.console import RenderableType
from rich.style import Style
from rich.text import Text

from spiel import Deck, Slide

deck = Deck(name="Deck Name")


def make_slide(
    title_prefix: str,
    text: Text,
) -> Slide:
    def content() -> RenderableType:
        return Align(text, align="center", vertical="middle")

    return Slide(title=f"{title_prefix} Slide", content=content)


deck.add_slides(
    make_slide(title_prefix="First", text=Text("Foo", style=Style(color="blue"))),
    make_slide(title_prefix="Second", text=Text("Bar", style=Style(color="red"))),
    make_slide(title_prefix="Third", text=Text("Baz", style=Style(color="green"))),
)

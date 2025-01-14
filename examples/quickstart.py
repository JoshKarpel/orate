from rich.console import RenderableType

from spiel import Deck, present

deck = Deck(name="Your Deck Name")


@deck.slide(title="Slide 1 Title")
def slide_1() -> RenderableType:
    return "Your content here!"


if __name__ == "__main__":
    present(__file__)

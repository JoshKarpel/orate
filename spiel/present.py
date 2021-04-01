import sys
from itertools import islice
from math import ceil

from rich.layout import Layout
from rich.live import Live
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style

from .exceptions import UnknownModeError
from .footer import Footer
from .input import handle_input, no_echo
from .modes import Mode
from .state import State
from .utils import clamp, joinify


def present_deck(state: State) -> None:
    footer = Layout(Footer(state), name="footer", size=1)
    console = state.console

    def get_renderable() -> Layout:
        current_slide = state.deck[state.current_slide_idx]

        body = Layout(name="body", ratio=1)
        if state.mode is Mode.SLIDE:
            body.update(Padding(current_slide.content, pad=1))
        elif state.mode is Mode.DECK:
            grid_width = state.deck_grid_width
            row_of_current_slide = state.current_slide_idx // grid_width
            num_rows = ceil(len(state.deck) / grid_width)
            start_row = clamp(
                value=row_of_current_slide - (grid_width // 2),
                lower=0,
                upper=num_rows - grid_width,
            )
            start_slide_idx = grid_width * start_row
            slides = islice(enumerate(state.deck.slides, start=1), start_slide_idx, None)

            rows = [Layout(name=str(r)) for r in range(grid_width)]
            cols = [
                [Layout(name=f"{r}-{c}") for c in range(grid_width)] for r, _ in enumerate(rows)
            ]

            body.split_column(*rows)
            for row, layouts in zip(rows, cols):
                for layout in layouts:
                    slide_number, slide = next(slides, (None, None))
                    if slide is None:
                        layout.update("")
                    else:
                        is_active_slide = slide is state.current_slide
                        layout.update(
                            Panel(
                                slide.content,
                                title=joinify(" | ", [slide_number, slide.title]),
                                border_style=Style(
                                    color="bright_cyan" if is_active_slide else None,
                                    dim=not is_active_slide,
                                ),
                            )
                        )
                row.split_row(*layouts)
        else:
            raise UnknownModeError(f"Unrecognized mode: {state.mode!r}")

        root = Layout(name="root")
        root.split_column(body, footer)

        return root

    with no_echo(), Live(
        get_renderable=get_renderable,
        console=console,
        screen=True,
        auto_refresh=True,
        refresh_per_second=10,
        vertical_overflow="visible",
    ) as live:
        try:
            while True:
                handle_input(state, sys.stdin)
                live.refresh()
        except Exception:
            live.stop()
            console.print_exception(show_locals=True)

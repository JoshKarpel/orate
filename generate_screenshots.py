#!/usr/bin/env python

import os
from collections.abc import Iterable
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from functools import partial
from io import StringIO
from pathlib import Path
from time import monotonic

from more_itertools import intersperse
from rich.console import Console
from rich.text import Text
from textual.app import App
from textual.pilot import Pilot

from spiel.app import SpielApp
from spiel.constants import DEMO_FILE
from spiel.triggers import Triggers

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "docs" / "assets"

# lie to Rich to make sure the screenshots are always generated in full color
os.environ["TERMCOLOR"] = "truecolor"

console = Console()


def take_reproducible_screenshot(app: App[object]) -> str:
    """
    Textual's screenshot functions don't let you control the unique_id argument to console.export_svg,
    so this little shim just reproduces the internals of Textual's methods with more control.
    """
    width, height = app.size
    renderer = Console(
        width=width,
        height=height,
        file=StringIO(),
        force_terminal=True,
        color_system="truecolor",
        record=True,
        legacy_windows=False,
    )
    screen_render = app.screen._compositor.render(full=True)
    renderer.print(screen_render)
    return renderer.export_svg(title=app.title, unique_id="spieldocs")


async def auto_pilot(pilot: Pilot[object], name: str, keys: Iterable[str]) -> None:
    await pilot.press(*intersperse("wait:50", keys), "wait:100")

    (ASSETS_DIR / name).with_suffix(".svg").write_text(take_reproducible_screenshot(pilot.app))

    await pilot.app.action_quit()


def take_screenshot(
    name: str,
    deck_file: Path,
    size: tuple[int, int],
    keys: Iterable[str],
    triggers: Triggers,
) -> str:
    console.print(Text.from_markup(f":camera: Generating [bold cyan]{name}[/bold cyan] ..."))

    SpielApp(
        deck_path=deck_file,
        watch_path=deck_file.parent,
        _show_messages=False,
        _fixed_time=datetime(year=2022, month=12, day=17, hour=15, minute=31, second=42),
        _fixed_triggers=triggers,
        _enable_transitions=False,
    ).run(
        headless=True,
        auto_pilot=partial(auto_pilot, name=name, keys=keys),
        size=size,
    )

    return name


if __name__ == "__main__":
    start_time = monotonic()

    demo_deck = DEMO_FILE
    quickstart_deck = ROOT_DIR / "docs" / "examples" / "quickstart.py"
    slide_via_decorator = ROOT_DIR / "docs" / "examples" / "slide_via_decorator.py"
    slide_loop = ROOT_DIR / "docs" / "examples" / "slide_loop.py"
    triggers_reveal = ROOT_DIR / "docs" / "examples" / "triggers_reveal.py"
    triggers_animation = ROOT_DIR / "docs" / "examples" / "triggers_animation.py"

    triggers = Triggers(now=0, _times=(0,))

    with ProcessPoolExecutor() as pool:
        futures = [
            pool.submit(
                take_screenshot,
                name="triggers_animation_1",
                deck_file=triggers_animation,
                size=(70, 15),
                keys=(),
                triggers=Triggers(now=0, _times=(0,)),
            ),
            pool.submit(
                take_screenshot,
                name="triggers_animation_2",
                deck_file=triggers_animation,
                size=(70, 15),
                keys=(),
                triggers=Triggers(now=1.5, _times=(0,)),
            ),
            pool.submit(
                take_screenshot,
                name="triggers_animation_3",
                deck_file=triggers_animation,
                size=(70, 15),
                keys=(),
                triggers=Triggers(now=2.5, _times=(0,)),
            ),
            pool.submit(
                take_screenshot,
                name="triggers_animation_4",
                deck_file=triggers_animation,
                size=(70, 15),
                keys=(),
                triggers=Triggers(now=5.5, _times=(0,)),
            ),
            pool.submit(
                take_screenshot,
                name="demo",
                deck_file=demo_deck,
                size=(130, 35),
                keys=(),
                triggers=triggers,
            ),
            pool.submit(
                take_screenshot,
                name="deck",
                deck_file=demo_deck,
                size=(135, 40),
                keys=("d", "right", "down"),
                triggers=triggers,
            ),
            pool.submit(
                take_screenshot,
                name="help",
                deck_file=demo_deck,
                size=(110, 35),
                keys=("?",),
                triggers=triggers,
            ),
            pool.submit(
                take_screenshot,
                name="quickstart_basic",
                deck_file=quickstart_deck,
                size=(70, 20),
                keys=(),
                triggers=triggers,
            ),
            pool.submit(
                take_screenshot,
                name="quickstart_code",
                deck_file=demo_deck,
                size=(140, 45),
                keys=("right",),
                triggers=triggers,
            ),
            pool.submit(
                take_screenshot,
                name="slide_via_decorator",
                deck_file=slide_via_decorator,
                size=(60, 15),
                keys=(),
                triggers=triggers,
            ),
            pool.submit(
                take_screenshot,
                name="slide_loop_1",
                deck_file=slide_loop,
                size=(60, 15),
                keys=(),
                triggers=triggers,
            ),
            pool.submit(
                take_screenshot,
                name="slide_loop_2",
                deck_file=slide_loop,
                size=(60, 15),
                keys=("right",),
                triggers=triggers,
            ),
            pool.submit(
                take_screenshot,
                name="slide_loop_3",
                deck_file=slide_loop,
                size=(60, 15),
                keys=("right", "right"),
                triggers=triggers,
            ),
            pool.submit(
                take_screenshot,
                name="triggers_reveal_1",
                deck_file=triggers_reveal,
                size=(70, 15),
                keys=(),
                triggers=Triggers(now=0, _times=(0,)),
            ),
            pool.submit(
                take_screenshot,
                name="triggers_reveal_2",
                deck_file=triggers_reveal,
                size=(70, 15),
                keys=(),
                triggers=Triggers(now=1, _times=(0, 1)),
            ),
            pool.submit(
                take_screenshot,
                name="triggers_reveal_3",
                deck_file=triggers_reveal,
                size=(70, 15),
                keys=(),
                triggers=Triggers(now=2, _times=(0, 1, 2)),
            ),
        ]

        for future in as_completed(futures, timeout=60):
            console.print(
                Text.from_markup(
                    f":camera_with_flash: Generated [bold cyan]{future.result()}[/bold cyan]"
                )
            )

    end_time = monotonic()

    console.print(
        Text.from_markup(
            f"Generated [green]{len(futures)}[/green] screenshots in [green]{end_time - start_time:0.2f}[/green] seconds"
        )
    )

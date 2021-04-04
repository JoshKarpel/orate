import shutil
from contextlib import nullcontext
from pathlib import Path

from rich.console import Console
from rich.style import Style
from rich.syntax import Syntax
from rich.text import Text
from typer import Argument, Exit, Option, Typer

from spiel.help import version_details
from spiel.load import DeckReloader, DeckWatcher, load_deck
from spiel.modes import Mode
from spiel.present import present_deck
from spiel.state import State

THIS_DIR = Path(__file__).resolve().parent

app = Typer()


@app.command()
def present(
    path: Path = Argument(..., dir_okay=False, help="The path to the slide deck file."),
    mode: Mode = Option(default=Mode.SLIDE, help="The mode to start presenting in."),
    watch: bool = Option(
        default=False, help="If enabled, reload the deck when the slide deck file changes."
    ),
    poll: bool = Option(
        default=False,
        help="If enabled, poll the filesystem for changes (implies --watch). Use this option on systems that don't support file modification notifications.",
    ),
) -> None:
    """
    Present a deck.
    """
    _present(path=path, mode=mode, watch=watch, poll=poll)


def _present(path: Path, mode: Mode, watch: bool, poll: bool) -> None:
    state = State(
        console=Console(),
        deck=load_deck(path),
        mode=mode,
    )

    watcher = (
        DeckWatcher(event_handler=DeckReloader(state, path), path=path, poll=poll)
        if (watch or poll)
        else nullcontext()
    )

    try:
        with watcher:
            present_deck(state)
    except KeyboardInterrupt:
        raise Exit(code=0)


@app.command()
def version() -> None:
    """
    Display version information for spiel and critical dependencies.
    """
    console = Console()

    console.print(version_details(console))


demo = Typer(
    name="demo",
    help="Use the demonstration deck (present it, display source, etc.)",
)

DEMO_DIR = THIS_DIR / "demo"
DEMO_SOURCE = THIS_DIR / "demo" / "demo.py"


@demo.command(name="present")
def present_demo() -> None:
    """
    Present the demo deck.
    """
    _present(path=DEMO_SOURCE, mode=Mode.SLIDE, watch=False, poll=False)


@demo.command()
def source() -> None:
    """
    Display the source code for the demo deck in your PAGER.
    """
    console = Console()

    with console.pager(styles=True):
        console.print(Syntax(DEMO_SOURCE.read_text(), lexer_name="python"))


@demo.command()
def copy(
    path: Path = Argument(
        default=...,
        writable=True,
        help="The path to copy the demo deck source code and assets to.",
    )
) -> None:
    """
    Copy the demo deck source code and assets to a new directory.
    """
    console = Console()

    if path.exists():
        console.print(Text(f"Error: {path} already exists!", style=Style(color="red")))
        raise Exit(code=2)

    try:
        shutil.copytree(DEMO_DIR, path)
    except Exception as e:
        console.print(Text(f"Failed to copy demo deck directory: {e}", style=Style(color="red")))
        raise Exit(code=1)

    console.print(
        Text(f"Wrote demo deck source code and assets to {path}", style=Style(color="green"))
    )


app.add_typer(demo)

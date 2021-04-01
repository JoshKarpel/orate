import sys
import traceback
from io import StringIO
from pathlib import Path
from textwrap import dedent
from typing import Callable, List, Union

import pytest
from click.testing import Result
from rich.console import Console
from typer.testing import CliRunner

from spiel.main import app
from spiel.slides import Deck, Slide
from spiel.state import State

CLI = Callable[[List[Union[str, Path]]], Result]


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def cli(runner: CliRunner) -> CLI:
    def invoker(args: List[Union[str, Path]]) -> Result:
        real_args = [str(arg) for arg in args if arg]
        print(real_args)
        result = runner.invoke(app, real_args)
        print("result:", result)

        if result.exc_info is not None:  # pragma: debugging
            print("traceback:\n")
            exc_type, exc_val, exc_tb = result.exc_info
            traceback.print_exception(exc_val, exc_val, exc_tb, file=sys.stdout)
            print()

        print("exit code:", result.exit_code)
        print("output:\n", result.output)
        return result

    return invoker


@pytest.fixture
def three_slide_deck() -> Deck:
    deck = Deck(name="three-slides")
    deck.add_slides(Slide(), Slide(), Slide())
    return deck


@pytest.fixture
def output() -> StringIO:
    return StringIO()


@pytest.fixture
def console(output: StringIO) -> Console:
    return Console(
        file=output,
        force_terminal=True,
        width=80,
    )


@pytest.fixture
def three_slide_state(console: Console, three_slide_deck: Deck) -> State:
    return State(console=console, deck=three_slide_deck)


@pytest.fixture
def empty_deck_source() -> str:
    return dedent(
        """\
        from spiel import Deck

        DECK = Deck(name="deck")
        """
    )


@pytest.fixture
def empty_file(tmp_path: Path) -> Path:
    file = tmp_path / "test_deck.py"

    file.touch()

    return file


@pytest.fixture
def file_with_empty_deck(empty_file: Path, empty_deck_source: str) -> Path:
    empty_file.write_text(empty_deck_source)

    return empty_file

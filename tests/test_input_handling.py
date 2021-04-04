from io import StringIO

import pytest

from spiel.exceptions import DuplicateInputHandler
from spiel.input import (
    SPECIAL_CHARACTERS,
    InputHandlers,
    SpecialCharacters,
    get_character,
    input_handler,
)
from spiel.state import State


@pytest.fixture
def handlers() -> InputHandlers:
    return {}  # type: ignore


def test_register_already_registered_raises_error(handlers: InputHandlers) -> None:
    @input_handler("a", help="")
    def a(state: State) -> None:  # pragma: never runs
        pass

    with pytest.raises(DuplicateInputHandler):

        @input_handler("a", help="")
        def a(state: State) -> None:  # pragma: never runs
            pass


@pytest.mark.parametrize("input, expected", SPECIAL_CHARACTERS.items())
def test_get_character_recognizes_special_characters(
    input: str, expected: SpecialCharacters
) -> None:
    io = StringIO(input)

    assert get_character(io) == expected
